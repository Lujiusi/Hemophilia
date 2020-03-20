# -*- coding: utf-8 -*-
# Author:RicardoM

from django import template

register = template.Library()


@register.simple_tag
def genderJudge(gender, value):
    if gender == value:
        print('checked')
        return 'checked'
    else:
        return ''
