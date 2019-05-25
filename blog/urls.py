# -*- coding: utf-8 -*-

"""kuzmin_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from blog.views import Privet, PostsListView, uno, PostDetailView, Post_YearArchiveView, Post_MonthArchiveView,\
    Post_DayArchiveView, CreateCommentView, RegistrationView, LoginView, UserRoom  #  newsite, Post,
from . import views
from django.views.generic.dates import ArchiveIndexView
from blog.forms import CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

app_name = 'blog'

urlpatterns = [
    url(r'^$', Privet.as_view(), name='home'), # содержит описание сайта  и показывает первые [:10]
    url(r'^index/$', uno.as_view(), name='index'),
    url(r'^blog/$', PostsListView.as_view(), name='list'),
    url(r'^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='simple_post'),
    url(r'^archive/(?P<year>\d{4})/$',  Post_YearArchiveView.as_view(),    name="Post_year_archive"), #1 pattern(s) tried: ['(<int:year>)/']

    # (?:page-(?P<page_number>\d+)/)?$',  Это пример из документации с вложенными аргументами

    #   url(r'^archive/(?P<year>\d{4})/(?P<month>\w+)/$',  Post_MonthArchiveView.as_view(month_format='%B'),    name="Post_month_archive"),
    #   r'^archive/(?P<year>\d{4})/(?:(\w+)-(?P<month>\d+)/)/$'
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d+)/$',   Post_MonthArchiveView.as_view(month_format='%m'),   name="month_numeric"),
    #   url(r'^archive/(?P<year>\d{4})/(?P<month>\w+)/(?P<day>\d+)/$',  Post_DayArchiveView.as_view(month_format='%B', day_format='%d'),    name="Post_day_archive"),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$', Post_DayArchiveView.as_view(month_format='%m', day_format='%d'),     name="Post_day_numeric"),
    url(r'^add_comment/$', CreateCommentView.as_view(), name='add_comment'),
    # url(r'^post/(?P<pk>\d+)/comment/$', CommentForm.as_view(), name='comment'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^login_now/$', LoginView.as_view(), name='login_view'),
    url(r'^userroom/(?P<user>[-\w]+)/$', UserRoom.as_view(), name='userroom'),
    url(r'^logout_now/$', LogoutView.as_view(next_page=reverse_lazy('blog:home')), name='logout'),
    url('^', include('django.contrib.auth.urls')),
]

