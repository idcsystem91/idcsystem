from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import StockData
from users.models import User
from django.utils import timezone
from .forms import StockForm, DeliveryForm, FindForm, StockDataCreateForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StockDataListForm
from django.db.models import Count, Q
import datetime
from django.http import HttpResponse
import csv


class Index(LoginRequiredMixin, TemplateView):
    """在庫管理トップページ"""
    template_name = "stocks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "在庫管理トップ"
        context['area'] = self.request.user.profile.default_area
        # context['area'] = self.request.session['area']
        context['job'] = self.request.user.profile.default_job
        # context['job'] = self.request.session['job']
        return context


"""ジェネリックビュー基本一式"""


class StockList(LoginRequiredMixin, ListView):
    model = StockData
    paginate_by: int = 50


class StockDetail(LoginRequiredMixin, DetailView):
    model = StockData


class StockCreate(LoginRequiredMixin, CreateView):
    template_name = "stocks/stockdata_form.html"
    form_class = StockForm
    success_url = reverse_lazy("list")


class StockUpdate(LoginRequiredMixin, UpdateView):
    template_name = "stocks/stockdata_form.html"
    model = StockData
    form_class = StockForm
    success_url = reverse_lazy("list")


class StockDelete(LoginRequiredMixin, DeleteView):
    model = StockData
    success_url = reverse_lazy("list")


"""ジェネリックビュー基本一式ここまで"""


"""マネージャー専用ページ"""


class ManagerIndex(TemplateView):
    template_name = "stocks/manager_index.html"


class ManagerStockList(StockList):
    template_name = "stocks/manager_stock_list.html"


class ManagerStockCount(TemplateView):
    template_name = 'stocks/manager_stock_count.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = StockData.objects.filter(Q(status__status_name='在庫') | Q(status__status_name='持出')).order_by('device__service', 'device__type', 'device__name', 'status').values(
            'device__service__name', 'device__type__name', 'device__name', 'status').annotate(Count('device'))
        return context


"""マネージャー専用ページここまで"""


class StockInStoreView(CreateView):
    """インスト出庫"""
    model = StockData
    form_class = StockDataCreateForm
    success_url = reverse_lazy("instore")
    template_name: str = "stocks/stockdata_createview.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["area"] = "練馬"
        initial["staff"] = self.request.user
        initial["status"] = 2
        return initial


class DefectiveList(StockList):
    """不良品リスト（ジェネリックビューのListを継承）"""

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = StockData.objects.filter(status__status_name="不良")
        return queryset


class CreateView(LoginRequiredMixin, CreateView):
    form_class = StockDataCreateForm
    model = StockData
    template_name = "stocks/stockdata_createview.html"

    def get_success_url(self):
        return reverse('create', kwargs={'pk': self.object.pk})


class UseDeviceUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "stocks/stock_update.html"
    model = StockData
    fields = ['serial', 'use', 'customer', 'status']
    success_url = reverse_lazy("used_list")

    def get_form(self):
        form = super(UseDeviceUpdateView, self).get_form()
        form.fields['serial'].widget.attrs['readonly'] = 'readonly'
        form.fields['use']
        form.fields['customer']
        form.fields['status']
        return form


class DeliveryView(LoginRequiredMixin, TemplateView):
    """在庫持出処理クラス"""

    def dispatch(self, request, *args, **kwargs):
        """初期設定項目"""
        # parse the request here ie.
        self.context = {
            'title': "出庫登録",
            'form': DeliveryForm,
            'area': self.request.user.profile.default_area,
            'job': self.request.user.profile.default_job,
        }
        # call the view
        return super(DeliveryView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """出庫処理のフォーム表示"""
        return render(request, 'stocks/delivery.html', self.context)

    def post(self, request):
        """データベース登録処理"""
        serial_no = request.POST['serial']  # フォームから受け取ったシリアルナンバーをserial_noに設定

        # シリアルナンバーの最初の文字が0または00だった場合、最初の0または00を削除する
        if serial_no[:2] == '00':
            serial_no = serial_no[2:]  # [2:]は文字列の3番目から最後までの意味(頭の２文字を削る)
        elif serial_no[0] == '0':
            serial_no = serial_no[1:]  # [1:]は文字列の２番目から最後までの意味(頭の1文字を削る)

        self.database = StockData

        if self.database.objects.filter(serial=serial_no, status_id=1).exists():
            # 受け取ったシリアルナンバーの在庫の状態が"在庫"になっているかを確認 # status_id=1は"在庫"
            obj = self.database.objects.get(serial=serial_no)
            obj.serial = serial_no
            obj.delivery = timezone.now()
            obj.staff = self.request.user
            obj.status_id = 2  # 2は持出
            # obj.log += timezone.now() + " : " + self.request.user + "が持出。/ "
            obj.save()

            self.context['device'] = obj.device
            self.context['serial'] = obj.serial

        elif self.database.objects.filter(serial=serial_no, status_id=2).exists():
            # 受け取ったシリアルナンバーの状態が持出済みになっていた場合
            self.context['warning'] = '未完了(持出済)'
            self.context['msg'] = serial_no + 'は既に<b>持出済み</b>です。'

        elif self.database.objects.filter(serial=serial_no, status_id=3).exists():
            # 受け取ったシリアルナンバーの状態が使用済みになっていた場合
            self.context['warning'] = '未完了(使用済)'
            self.context['msg'] = serial_no + 'は既に<b>使用済み</b>です。'

        else:
            # 受け取ったシリアルナンバーの状態が不良、返却済みになっている、またはシリアルが存在しない場合
            self.context['warning'] = '未完了(該当ID無し)'
            self.context['msg'] = serial_no + 'は在庫にありません。'

        return render(request, 'stocks/delivery.html', self.context)


class UseView(LoginRequiredMixin, TemplateView):
    """在庫持出処理クラス"""

    def dispatch(self, request, *args, **kwargs):
        """初期設定項目"""
        # parse the request here ie.
        self.context = {
            'title': "使用登録",
            'area': self.request.user.profile.default_area,
            'job': self.request.user.profile.default_job,
        }
        # call the view
        return super(UseView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        staff_id = self.request.user
        status = 2  # status_id 2 は持出済状態
        data = StockData.objects.select_related().values('id', 'device__id', 'device__service__name', 'device__service__sort_no',
                                                               'device__type__name', 'device__type__sort_no', 'device__name', 'serial').filter(staff=staff_id, status_id=status)
        self.context['data'] = data

        return render(request, 'stocks/use.html', self.context)

    def post(self, request):
        customer = request.POST['customer']
        use_date = request.POST['use']
        stock_id_list = request.POST.getlist('stock_id')
        status_no = 3  # 3は使用済

        for stock_id in stock_id_list:
            obj = StockData.objects.get(id=int(stock_id))
            obj.customer = customer
            obj.use = use_date
            obj.status_id = status_no
            obj.save()

        staff_id = self.request.user
        status = 2  # status_id 2 は持出済状態
        data = StockData.objects.select_related().values('id', 'device__id', 'device__service__name', 'device__service__sort_no',
                                                               'device__type__name', 'device__type__sort_no', 'device__name', 'serial').filter(staff=staff_id, status_id=status)
        self.context['data'] = data

        return render(request, 'stocks/use.html', self.context)


class ReturnView(LoginRequiredMixin, TemplateView):

    def __init__(self):
        self.context = {
            'title': "返却登録",
        }

    def get(self, request):
        staff_id = self.request.user
        status = 2  # status_id 2 は持出済状態
        data = StockData.objects.select_related().values('id', 'device__id', 'device__service__name', 'device__service__sort_no',
                                                               'device__type__name', 'device__type__sort_no', 'device__name', 'serial').filter(staff=staff_id, status_id=status)
        self.context['data'] = data

        return render(request, 'stocks/return.html', self.context)

    def post(self, request):
        now = timezone.now()
        date = now.strftime('%Y-%m-%d')
        status_id = request.POST.get('status')
        stock_id_list = request.POST.getlist('stock_id')

        for stock_id in stock_id_list:
            obj = StockData.objects.get(id=int(stock_id))
            obj.staff = None
            obj.delivery = None
            obj.status_id = status_id
            obj.log += "○ " + date + ":" + str(self.request.user) + "が返却 "
            obj.save()
            self.context['device'] = obj.device
            self.context['serial'] = obj.serial

        staff_id = self.request.user
        status = 2  # status_id 2 は持出済状態
        data = StockData.objects.select_related().values('id', 'device__id', 'device__service__name', 'device__service__sort_no',
                                                               'device__type__name', 'device__type__sort_no', 'device__name', 'serial').filter(staff=staff_id, status_id=status)
        self.context['data'] = data

        return render(request, 'stocks/return.html', self.context)


class FindView(LoginRequiredMixin, TemplateView):
    """在庫検索"""

    def dispatch(self, request, *args, **kwargs):
        """初期設定項目"""
        # parse the request here ie.
        self.context = {
            'title': "在庫検索",
            'area': self.request.user.profile.default_area,
            'job': self.request.user.profile.default_job,
            'form': FindForm
        }
        # call the view
        return super(FindView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'stocks/find.html', self.context)

    def post(self, request):
        self.context['form'] = FindForm(request.POST)
        serial_no = request.POST['serial']
        data = StockData.objects.filter(serial__contains=serial_no)
        msg = str(data.count()) + "件見つかりました"

        self.context['data'] = data
        self.context['msg'] = msg

        return render(request, 'stocks/find.html', self.context)


class StockDataDetailView(LoginRequiredMixin, DetailView):
    model = StockData
    template_name = 'stocks/detail.html'


class StockDataListView(ListView):
    template_name = "stocks/admin_stockdata_list.html"
    model = StockData
    paginate_by = 100

# class StockDataListView(LoginRequiredMixin, TemplateView):
#    template_name = 'stocks/list.html'
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['title'] = '在庫確認'
#        data = StockData.objects.select_related().values('device__id', 'device__service__name', 'device__service__sort_no',
#                                                         'device__type__name', 'device__type__sort_no', 'device__name', 'serial', 'status')
#        annotate_data = StockData.objects.annotate(
#            device=Count('device'))
#        context['data'] = data
#        context['annotate_data'] = annotate_data
#        return context


class StockDataFormView(FormView):
    template_name = "stocks/admin_stockdata_update.html"
    form_class = StockDataListForm
    success_url = '/stocks/'

    def form_valid(self, form):
        # このメソッドは、有効なフォームデータがPOSTされたときに呼び出されます。
        # HttpResponseを返す必要があります。
        form.send_email()
        return super().form_valid(form)


class StockDataCountView(TemplateView):
    template_name = 'stocks/data_count.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = StockData.objects.filter(Q(status__status_name='在庫') | Q(status__status_name='持出')).order_by('device__service', 'device__type', 'device__name', 'status').values(
            'device__service__name', 'device__type__name', 'device__name', 'status').annotate(Count('device'))
        return context


class StockDataDeviceStockListView(TemplateView):

    template_name = 'stocks/device_stock_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.kwargs.get('device')
        context['device'] = device
        context['data'] = StockData.objects.filter(
            device__name=device, status__status_name__in=['在庫', '持出']).values('serial', 'staff__username').order_by('staff__username')

        return context


class UsedDeviceListView(TemplateView):
    template_name = 'stocks/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.request.user
        one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        context['data'] = StockData.objects.filter(
            staff=staff, status__status_name='設置', use__range=[one_month_ago, datetime.datetime.now()]
        ).values('id', 'use', 'customer', 'device__name', 'serial').order_by('-use', 'customer', 'device__id')
        return context


class UserDeviceUpdate(StockUpdate):
    form_class = StockForm


""" 棚卸し用CSVファイル生成 """


class InventoryCSVExport(ListView):
    template_name = 'stocks/inventory_list.html'
    model = StockData

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = StockData.objects.filter(
            status__status_name__in=['在庫', '持出', '不良']).order_by('device')

        return context


def inventory_CSV_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asaka.csv"'
    writer = csv.writer(response)
    writer.writerow([""])
    for device in StockData.objects.filter(
        status__status_name__in=['在庫', '持出']
    ):
        writer.writerow([device.serial])
    return response


class UsedDevice(TemplateView):
    template_name = 'stocks/use_device_list.html'
    model = StockData

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.request.user
        context["data"] = StockData.objects.filter(staff=staff, status__status_name__in=[
                                                   '設置']).order_by("use", "customer").reverse()
        return context
