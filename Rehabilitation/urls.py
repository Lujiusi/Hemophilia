# -*- coding: utf-8 -*-
# Author:RicardoM

from django.urls import path

from Rehabilitation import views

urlpatterns = [

    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('article/<int:articleId>', views.article, name='article'),
    path('write/', views.write, name='write'),
    path('userProfile/<str:username>', views.UserProfile.as_view(), name='userProfile'),
    path('operateArticle', views.OperateArticle.as_view(), name='operateArticle'),
    path('messages/', views.messages, name='messages'),
    path('sendMessage/', views.sendMessage, name='sendMessage'),
    path('deleteConversation/', views.delete_conversation, name='deleteConversation'),
    path('modifyUser/', views.modify_profile, name='modifyProfile'),
    path('shieldUser/<str:convId>', views.shield_user, name='shieldUser'),
    path('test/', views.test),
    path('conversation/<str:convId>', views.conversation, name='conversation'),
    path('comment', views.comment, name='comment'),
    path('userPic/', views.UserPic.as_view(), name='userPic'),
    path('', views.index, name='index'),

]
