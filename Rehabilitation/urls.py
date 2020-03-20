# -*- coding: utf-8 -*-
# Author:RicardoM

from django.urls import path

from Rehabilitation import views

urlpatterns = [

    # path('user/login/', views.loginpage, name='loginpage'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('article/<int:articleId>', views.article, name='article'),
    path('write/', views.write, name='write'),
    path('userProfile/<str:username>', views.UserProfile.as_view(), name='userProfile'),
    path('operateArticle', views.OperateArticle.as_view(), name='operateArticle'),
    path('messages/', views.messages, name='messages'),
    path('conversation/<str:convId>/', views.conversation, name='conversation'),
    path('comment', views.comment, name='comment'),
    # path('contacts/', views.contacts, name='contacts'),
    # path('acc_logout/', views.acc_logout, name='acc_logout'),
    # path('userInfo/<int:userId>/', views.user_info, name='userInfo'),
    # path('create_conversation/', views.create_conversation, name='create_conversation'),
    # path('sessions/', views.sessions, name='sessions'),
    # path('password_change/', views.password_change, name='password_change'),
    # path('conversation/<str:convs_id>/', views.conversation, name='conversation'),
    path('', views.index, name='index'),

]
