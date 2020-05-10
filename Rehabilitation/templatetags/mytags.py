# -*- coding: utf-8 -*-
# Author:RicardoM

from django import template
from Rehabilitation.models import *

register = template.Library()


@register.simple_tag
def genderJudge(gender, value):
    if gender == value:
        print('checked')
        return 'checked'
    else:
        return ''


@register.simple_tag
def anotherPeople(current_user, conversation):
    if current_user == conversation.send_user:
        return conversation.accept_user
    else:
        return conversation.send_user


@register.simple_tag
def anotherName(current_user, conversation):
    if current_user == conversation.send_user:
        return conversation.accept_user.nickname
    else:
        return conversation.send_user.nickname


@register.simple_tag
def likeCount(article):
    return len(Comment.objects.filter(article=article, comment_type=2))


@register.simple_tag
def commentCount(article):
    return len(Comment.objects.filter(article=article, comment_type=1))


@register.simple_tag
def fixPath(avatar):
    return "/media/%s" % (avatar)
