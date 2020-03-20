from django.contrib import admin

from .models import *


# Register your models here.

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
