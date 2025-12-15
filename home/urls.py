from django.contrib import admin
from django.urls import path
from home import views
from home import auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('signup', auth_views.signup_view, name='signup'),
    path('login', auth_views.login_view, name='login'),
    path('logout', auth_views.logout_view, name='logout'), 
    path('createBlog', views.createBlog, name='createBlog'),
]
