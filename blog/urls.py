from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('<slug:slug>/', views.blogPost, name='blogPost'),

    # API to post a comment
    path('postComment', views.postComment, name='postComment'),
]
