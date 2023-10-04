from django import forms
from .models import Concurrent

class ConcurrentForm(forms.ModelForm):
    in_university = forms.BooleanField(label="Are you in University right now?", required=False)
    sex = forms.ChoiceField(label="Sex", widget=forms.RadioSelect, choices=Concurrent.SEX_CHOICES)

    class Meta:
        model = Concurrent
        fields = ['lastname', 'firstname', 'sex', 'in_university', 'university', 'discipline', 'level', 'profession', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
class ConcurrentLoginForm(forms.Form):
    code = forms.CharField(max_length=25, label='Code')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')