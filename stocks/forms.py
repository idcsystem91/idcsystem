from django import forms
from django.utils import timezone
from .models import StockData

class StockForm(forms.ModelForm):
    class Meta:
        model = StockData
        fields = "__all__"


#class StockForm(forms.ModelForm):
#    class Meta:
#        model=StockData
#        fields="__all__"


class StockDataCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['area'].widget = forms.HiddenInput()
        self.fields['device']
        self.fields['serial']
        self.fields['arrival'].initial = timezone.now()
        self.fields['delivery'].initial = timezone.now()
        self.fields['staff'].widget = forms.HiddenInput()
        self.fields['job'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()
        

    class Meta:
        model = StockData
        fields = ("area", "device", "serial", "arrival",
                  "delivery", "staff", "job", "status")
        # widgets = {
        #    'area': forms.(attrs={'placeholder': '1'})
        # }


class DeliveryForm(forms.Form):
    serial = forms.CharField(
        label='機器ID',
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))


class FindForm(forms.Form):
    serial = forms.CharField(
        label='機器ID(部分入力での検索可)',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))


class UseForm(forms.Form):
    pass

    """
    def __init__(self, data, *args, **kwargs):
        self.device_data = data
        super().__init__(*args, **kwargs)

    customer = forms.CharField(
        label='顧客番号',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control pattern="[0-9]{8}"'})
    )

    use = forms.DateField(
        label='使用日',
        required=True,
        input_formats=['%Y-%m-%d'],
        initial=timezone.now(),
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

    stock_id = forms.BooleanField(
        label=self.data.serial,
        initial=self.data.id,
        widget=forms.CheckboxInput(attrs={'class': 'form-control'})
    )
"""


class StockDataListForm(forms.ModelForm):
    class Meta:
        model = StockData
        fields = '__all__'
