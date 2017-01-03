# -*- coding: UTF-8 -*-
from captcha.fields import ReCaptchaField
from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class SubmitForm(forms.Form):
    repository_url = forms.URLField(validators=[
        RegexValidator(regex=r'https://github.com/[^/]+/[^/]+/?$', message=_('Invalid GitHub URL'),
                       code='github_url')])
    captcha = ReCaptchaField()
