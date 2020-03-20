# -*- coding: utf-8 -*-
# Author:RicardoM
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget


class MessageForm(forms.Form):
    article_from = forms.CharField(widget=SummernoteInplaceWidget())
