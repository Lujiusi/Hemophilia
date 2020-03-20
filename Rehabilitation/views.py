import json, time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.template.loader import render_to_string
from Rehabilitation import form
from .models import *


def index(request):
    article_list = Article.objects.all()
    return render(request, 'Rehabilitation/index.html', locals())


class Register(View):

    @staticmethod
    def post(request):
        r = User()
        r.username = request.POST['username']
        r.password = request.POST['password']
        r.realname = request.POST.get('realname', '')
        r.nickname = request.POST.get('nickname', '')
        r.avatar = request.FILES.get('avatar', None)
        r.gender = request.POST.get('gender', '')
        r.phone = request.POST.get('phone', '')
        r.email = request.POST.get('email', '')
        res = {
            'status': '',
            'errorMsg': '',
        }
        # 判断用户名是否存在
        if User.objects.filter(username=r.username):
            res['status'] = '0'
            res['errorMsg'] = '该用户名已经存在，请重新输入!'
        else:
            res['status'] = '1'
            r.password = make_password(r.password)
            r.save()
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


class Login(View):

    @staticmethod
    def post(request):
        res = {}
        u = User()
        u.username = request.POST['username']
        u.password = request.POST['password']
        u.remember_me = request.POST.get('remember_me', 'true')
        user = authenticate(username=u.username, password=u.password)
        if user is None:
            res['status'] = '0'
        else:
            login(request, user)
            res['status'] = '1'
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


@login_required
def comment(request):
    article_id = request.POST.get('article_id', request.GET['article_id'])
    com = request.POST.get('comment')
    to_comment = request.POST.get('to_comment')
    new_comment = Comment()
    new_comment.user = request.user
    new_comment.article = Article.objects.filter(id=article_id)[0]
    if com:
        new_comment.comment = com
        new_comment.comment_type = '1'
    else:
        new_comment.comment_type = '2'
    if to_comment:
        new_comment.parent_comment = Comment.objects.filter(id=to_comment)[0]
    if new_comment.comment_type == '2':
        Comment.objects.filter(comment_type="2", article=new_comment.article, user=request.user).delete()
    else:
        new_comment.save()
    return redirect(reverse('Rehabilitation:article', kwargs={'articleId': article_id}))


class Logout(View):

    @staticmethod
    @login_required
    def get(request):
        next = request.GET['next']
        logout(request)
        response = redirect(next)
        if 'username' in request.COOKIES:
            response.delete_cookie('username')
        return response


def article(request, articleId):
    art = Article.objects.filter(id=articleId)[0]
    comment_list = {}
    for comment in Comment.objects.filter(article=art, parent_comment=None).order_by('date').all():
        if comment not in comment_list:
            comment_list[comment] = []
        for com in Comment.objects.filter(parent_comment=comment).order_by('date').all():
            comment_list[comment].append(com)
    for comment, comment_list1 in comment_list.items():
        comment_list1.extend(findComment(comment_list1))
    had_like = Comment.objects.filter(comment_type='2', user=request.user)
    return render(request, 'Rehabilitation/article.html', locals())


@login_required
def write(request):
    article_Form = form.MessageForm
    return render(request, 'Rehabilitation/write.html', locals())


class UserProfile(View):

    @staticmethod
    def get(request, username):
        if request.user.is_authenticated:
            current_user = request.user
        u = User.objects.filter(username=username)[0]
        return render(request, 'Rehabilitation/userProfile.html', locals())

    @staticmethod
    @login_required
    def post(request):
        pass


class OperateArticle(View):

    @staticmethod
    @login_required
    def post(request):
        article = Article()
        article.title = request.POST['title']
        article.brief = request.POST['brief']
        article.content = request.POST['article_from']
        article.status = request.POST['status']
        article.author = request.user
        article.category = Category.objects.filter(id='1')[0]
        article.priority = 1
        if article.status == 'published':
            article.pub_date = time.time()
        else:
            article.status = 'published'
        article.save()
        return redirect(reverse('Rehabilitation:article', kwargs={'articleId': article.id}))


def messages(request):
    return render(request, 'Rehabilitation/messages.html')


def conversation(request, convId):
    return render(request, 'Rehabilitation/conversation.html')


def findComment(comment_list):
    com_list = []
    for comment in comment_list:
        com_list1 = []
        for com1 in Comment.objects.filter(parent_comment=comment).all():
            com_list1.append(com1)
        com_list.extend(com_list1)
        if len(com_list1) > 0:
            com_list.extend(findComment(com_list1))
    return com_list
