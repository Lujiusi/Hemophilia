from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *


# Register your models here.

# Apply summernote to all TextField in model.
class Article_summer(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('content')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'realname', 'signature', 'nickname', 'avatar', 'gender', 'phone', 'email', 'city']
    list_display_links = list_display
    ordering = ['-id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'brief', 'set_as_top_menu', 'position_index']
    list_display_links = list_display
    ordering = ['-id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'parent_comment', 'comment_type', 'user', 'comment', 'date']
    list_display_links = list_display
    ordering = ['-id']


@admin.register(Article)
class ArticleAdmin(Article_summer):
    list_display = ['id', 'title', 'brief', 'category', 'content', 'author', 'pub_date', 'last_modify', 'priority',
                    'status']
    list_display_links = list_display
    ordering = ['-id']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'send_user', 'accept_user', 'is_delete_by_sendPeople', 'is_delete_by_acceptPeople',
                    'creation_time']
    list_display_links = list_display
    ordering = ['-id']


@admin.register(Massage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'send_user', 'accept_user', 'msg_detail', 'send_date']
    list_display_links = list_display
    ordering = ['-id']
