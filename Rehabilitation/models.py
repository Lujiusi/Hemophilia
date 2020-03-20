from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.exceptions import ValidationError


# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # 用户表 用户信息 用户名 用户签名 用户头像
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    signature = models.CharField(verbose_name='签名', max_length=255, blank=True, null=True)
    avatar = models.ImageField(verbose_name='用户头像', blank=True, upload_to='static/userpic')
    realname = models.CharField(verbose_name='姓名', max_length=32, default='', null=True)
    gender = models.CharField(verbose_name='性别', max_length=10, choices=(('男', '男'), ('女', '女')), default='男')
    phone = models.CharField(verbose_name='手机号码', max_length=64, default='', null=True)
    email = models.CharField(verbose_name='Email', max_length=64, default='', null=True)
    city = models.CharField(verbose_name='所在城市', max_length=32, default='', null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    class Meta:
        verbose_name = '帖子分类'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # 文章类型表 名称 简要 是否为置顶 热度 管理员
    id = models.AutoField('主键id', primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    brief = models.CharField(null=True, blank=True, max_length=64)
    set_as_top_menu = models.BooleanField(default=False)
    position_index = models.SmallIntegerField()

    def __str__(self):
        return self.name


class Article(models.Model):
    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # 创建文章表 标题 简介 标题图片 类型 内容 作者 发布时间 最后修改时间 优先级 状态(发布or草稿)
    id = models.AutoField('主键id', primary_key=True)
    title = models.CharField(max_length=255)
    brief = models.CharField(null=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField(u'文章内容')
    author = models.ForeignKey(to='User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(blank=True, null=True)
    last_modify = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(u'优先级')
    status_choices = (
        ('draft', u'草稿'),
        ('published', u'已发布'),
        ('hidden', u'隐藏'),
    )
    status = models.CharField(choices=status_choices, default='published', max_length=32)

    def __str__(self):
        return self.title

    def clean(self):
        # 不允许草稿内容有发布时间
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError('Draft entries may not have a publication date.')
        # 当文章发布时设置发布时间
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()


class Comment(models.Model):
    class Meta:
        verbose_name = '评论或点赞'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # 评论表or点赞  所属文章 所属父评论 类型(评论or点赞) 评论者 评论内容 评论时间
    id = models.AutoField('主键id', primary_key=True)
    article = models.ForeignKey(Article, verbose_name=u'所属文章', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(to='self', related_name='my_children', blank=True, null=True,
                                       on_delete=models.CASCADE)
    comment_choices = (
        (1, u'评论'),
        (2, u'点赞'),
    )
    comment_type = models.IntegerField(choices=comment_choices, default=1)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return "T : %s TO: %s" % (self.article.title, self.comment)

    def clean(self):
        # 评论类型为评论,且评论内容为空 发出错误
        if self.comment_type == 1 and len(self.comment) == 0:
            raise ValidationError('Comment not be null! SB')


# 	会话表:
# 		会话Id:
# 		发起者 id:
# 		接收者 id:
# 		是否匿名 : boolean
# 		被p1 删除: boolean
# 		被p2 删除: boolean
# 		创建时间 : date

class Conversation(models.Model):
    class Meta:
        verbose_name = '会话内容'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    id = models.AutoField('主键id', primary_key=True)
    send_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="conversation_send_user")
    accept_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="conversation_accept_user")
    # 此处不好,每当这个会话中添加新的session 此两处被重置为false;
    is_delete_by_sendPeople = models.BooleanField(default=False)
    is_delete_by_acceptPeople = models.BooleanField(default=False)
    creation_time = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return "%s To %s" % (str(self.send_user.username), str(self.accept_user.username))


# 	消息列表:
# 		消息id:
# 		所在会话id:
# 		说话人 p1 :
# 		说话人 p2:
# 		时间 : date
class Massage(models.Model):
    class Meta:
        verbose_name = '聊天内容'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    id = models.AutoField('主键id', primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    send_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='massage_send_user')
    accept_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='massage_accept_user')
    msg_detail = models.TextField(blank=False, null=False)
    send_date = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return self.msg_detail


class Blacklist(models.Model):
    class Meta:
        verbose_name = '屏蔽会话用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    id = models.AutoField('主键id', primary_key=True)
    master_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='master_user')
    black_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='black_user')
    black_date = models.DateTimeField(verbose_name='点赞时间', auto_now_add=True)

    def __str__(self):
        return '%s blocked %s' % (self.master_user.username, self.black_user.nickname)
