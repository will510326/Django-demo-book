from django import forms
from captcha.fields import CaptchaField


class PostForm(forms.Form):
    username = forms.CharField(max_length=20, initial='')
    pd = forms.CharField(max_length=20, initial='')
    captcha = CaptchaField()
