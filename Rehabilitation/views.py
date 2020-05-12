import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.template.loader import render_to_string
from django.utils import timezone
from Rehabilitation import form
from PIL import Image
from .models import *
from io import BytesIO


def index(request):
    article_list = Article.objects.filter(status="published")
    return render(request, 'Rehabilitation/index.html', locals())


class Register(View):

    @staticmethod
    def post(request):
        r = User()
        r.username = request.POST['username']
        r.password = request.POST['password']
        r.realname = request.POST.get('realname', '')
        r.nickname = request.POST.get('nickname', r.username)
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
    if request.POST.get('article_id'):
        article_id = request.POST.get('article_id')
    else:
        article_id = request.GET.get('article_id')
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
        like_comment = Comment.objects.filter(comment_type="2", article=new_comment.article, user=request.user)
        print(like_comment)
        if len(like_comment) > 0:
            print(len(like_comment))
            like_comment[0].delete()
        else:
            new_comment.save()
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
    for comment in Comment.objects.filter(article=art, comment_type='1', parent_comment=None).order_by('date').all():
        if comment not in comment_list:
            comment_list[comment] = []
        for com in Comment.objects.filter(parent_comment=comment).order_by('date').all():
            comment_list[comment].append(com)
    for comment, comment_list1 in comment_list.items():
        comment_list1.extend(findComment(comment_list1))
    if request.user.is_authenticated:
        had_like = Comment.objects.filter(comment_type='2', user=request.user, article__id=articleId)
    return render(request, 'Rehabilitation/article.html', locals())


@login_required
def write(request):
    article_Form = form.MessageForm
    category_list = Category.objects.all()
    return render(request, 'Rehabilitation/write.html', locals())


class UserProfile(View):

    @staticmethod
    def get(request, username):
        if request.user.is_authenticated:
            current_user = request.user
        u = User.objects.filter(username=username)[0]
        print(u.avatar)
        pub_article = Article.objects.filter(author=u, status="published")
        dra_article = Article.objects.filter(author=u, status="draft")
        return render(request, 'Rehabilitation/userProfile.html', locals())

    @staticmethod
    @login_required
    def post(request):
        pass


class OperateArticle(View):

    @staticmethod
    @login_required
    def get(request):
        current_user = request.user
        article_id = request.GET.get('article_id')
        category_list = Category.objects.all()
        article = Article.objects.filter(id=article_id)[0]
        return render(request, 'Rehabilitation/reEditArticle.html', locals())

    @staticmethod
    @login_required
    def post(request):
        article_id = request.POST.get('article_id')
        article = Article()
        if article_id:
            article = Article.objects.filter(id=article_id)[0]
        article.title = request.POST['title']
        article.brief = request.POST['brief']
        article.category_id = request.POST['category']
        article.content = request.POST['article_from']
        article.status = request.POST['status']
        article.author = request.user
        article.category = Category.objects.filter(id='1')[0]
        article.priority = 1
        if article.status == 'published':
            article.pub_date = timezone.now()
        else:
            article.status = 'draft'
        article.last_modify = timezone.now()
        article.save()
        return redirect(reverse('Rehabilitation:article', kwargs={'articleId': article.id}))


@login_required
def messages(request):
    send_user = request.user
    accept_user_id = request.GET.get('user_id')
    if accept_user_id:
        accept_user = User.objects.filter(username=accept_user_id)[0]
        isShield = Blacklist.objects.filter(master_user=send_user, black_user=accept_user)
        if len(isShield) > 0:
            isShield[0].delete()
        a = Conversation.objects.filter(send_user=send_user, accept_user=accept_user)
        b = Conversation.objects.filter(send_user=accept_user, accept_user=send_user)
        conv = None
        if len(a) > 0:
            conv = a[0]
            conv.is_delete_by_sendPeople = False
        elif len(b) > 0:
            conv = b[0]
            conv.is_delete_by_acceptPeople = False
        else:
            conv = Conversation.objects.create(send_user=send_user, accept_user=accept_user)
        conv.save()
        return redirect(reverse('Rehabilitation:conversation', kwargs={'convId': conv.id}))
    else:
        conversation_list = Conversation.objects.filter(
            Q(send_user=send_user, is_delete_by_sendPeople=False) | Q(accept_user=send_user,
                                                                      is_delete_by_acceptPeople=False))
        return render(request, 'Rehabilitation/messages.html', locals())


@login_required
def sendMessage(request):
    conv_id = request.POST.get('conv_id')
    conv = Conversation.objects.filter(id=conv_id)[0]
    current_user = request.user
    another_user = get_other_user(current_user, conv)
    if len(Blacklist.objects.filter(master_user=another_user, black_user=current_user)) < 1:
        message_detail = request.POST.get('message_detail')
        conv.last_send_time = timezone.now()
        conv.save()
        mess = Massage.objects.create(conversation=conv, send_user=current_user, accept_user=another_user,
                                      msg_detail=message_detail)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("abc%s" % another_user.id,
                                                generate_payload(current_user, mess))
        async_to_sync(channel_layer.group_send)("abc%s" % current_user.id,
                                                generate_payload(current_user, mess))
        res = dict(is_success=True)
    else:
        res = dict(is_success=False)
    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json')


@login_required
def conversation(request, convId):
    current_user = request.user
    another_user = None
    conv = Conversation.objects.filter(id=convId)[0]
    if conv.send_user == current_user:
        another_user = conv.accept_user
    else:
        another_user = conv.send_user
    conv_list = Massage.objects.filter(conversation=conv)
    return render(request, 'Rehabilitation/conversation.html', locals())


@login_required
def delete_conversation(request):
    convId = request.GET.get('conv_id')
    current_user = request.user
    min_delete_conversation(convId, current_user)
    return redirect(reverse('Rehabilitation:messages'))


@login_required
def shield_user(request, convId):
    conv = Conversation.objects.filter(id=convId)[0]
    current_user = request.user
    other_user = get_other_user(current_user, conv)
    Blacklist.objects.create(master_user=current_user, black_user=other_user)
    min_delete_conversation(convId, current_user)
    return redirect(reverse('Rehabilitation:messages'))


def min_delete_conversation(convId, current_user):
    conv = Conversation.objects.filter(id=convId)[0]
    if current_user == conv.send_user:
        conv.is_delete_by_sendPeople = True
    else:
        conv.is_delete_by_acceptPeople = True
    conv.save()


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


@login_required
def modify_profile(request):
    current_user = request.user
    fieldname = request.POST.get('name')
    fieldvalue = request.POST.get('value')
    if fieldname == 'nickname':
        current_user.nickname = fieldvalue
    elif fieldname == 'gender':
        current_user.gender = fieldvalue
    elif fieldname == 'realname':
        current_user.realname = fieldvalue
    elif fieldname == 'mail':
        current_user.email = fieldvalue
    elif fieldname == 'phone':
        current_user.phone = fieldvalue
    elif fieldname == 'city':
        current_user.city = fieldvalue
    elif fieldname == 'signature':
        current_user.signature = fieldvalue
    current_user.save()
    return HttpResponse(json.dumps({}, ensure_ascii=False), content_type='application/json')


def get_other_user(current_user, current_conv):
    if current_user == current_conv.send_user:
        other_user = current_conv.accept_user
    else:
        other_user = current_conv.send_user
    return other_user


def generate_payload(user, message_detail):
    payload = {
        'type': 'receive',
        'massage': render_to_string('Rehabilitation/simple_message.html',
                                    {'message_detail': message_detail, 'current_user': user}),
    }
    return payload


def test(request):
    return render(request, 'Rehabilitation/test.html')


class UserPic(View):

    @staticmethod
    @login_required
    def post(request):
        file = request.FILES['avatar_file']
        data = request.POST['avatar_data']
        img = crop_image(file, data)
        current_user = request.user
        current_user.avatar = img
        current_user.save()

        return HttpResponse(json.dumps({'result': True}, ensure_ascii=False), content_type='application/json')


def crop_image(file, data):
    coords = json.loads(data)
    t_x = int(coords['x'])
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']

    # 裁剪图片,压缩尺寸为400*400。
    img = Image.open(file)
    crop_im = img.crop((t_x, t_y, t_width, t_height)).resize((400, 400), Image.ANTIALIAS).rotate(t_rotate)

    pic_io = BytesIO()
    crop_im.save(pic_io, img.format)
    crop_im = InMemoryUploadedFile(
        file=pic_io,
        field_name=None,
        name=file.name,
        content_type=None,
        size=crop_im.size,
        charset=None
    )

    return crop_im
