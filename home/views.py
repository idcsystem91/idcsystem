from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, TemplateView):
    """メインメニュー"""
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        # """セッション変数'area'が空の場合にデフォルトのエリア名を設定する"""
        # if not 'area' in self.request.session:
        #    self.request.session['area'] = self.request.user.profile.default_area.name

        # """セッション変数'job'が空の場合にデフォルトの業務名を設定する"""
        # if not 'job' in self.request.session:
        #    self.request.session['job'] = self.request.user.profile.default_job.name

        context = super().get_context_data(**kwargs)
        context['subtitle'] = "メインメニュー"
        context['user'] = self.request.user.id
        context['area'] = self.request.user.profile.default_area
        #context['area'] = self.request.session.get('area')
        context['job'] = self.request.session.get('job')
        return context
