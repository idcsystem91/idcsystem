from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """プロフィール変更ページ用フォーム"""
    class Meta:
        model = Profile
        fields = ('id', 'last_name', 'first_name', 'birthday', 'phone',
                  'phone_type', 'office', 'default_area', 'default_job')

        labels = {
            'phone': '携帯番号（ - を入れてください）'
        }
        widgets = {
            'birthday': forms.SelectDateWidget(years=[x for x in range(1950, 2031)]),
            'phone': forms.TextInput(attrs={'placeholder': '090-1234-5678'}),
        }
