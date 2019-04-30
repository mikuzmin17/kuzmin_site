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
from django.conf.urls import url
from blog.views import PostsListView, PostDetailView, Post_YearArchiveView, Privet #  newsite, Post
from . import views
from django.views.generic.dates import ArchiveIndexView
from blog.forms import CommentForm


app_name = 'blog'

urlpatterns = [
    url(r'^$', Privet.as_view(), name='home'), # содержит описание сайта  и показывает первые [:10]
    url(r'^blog/$', PostsListView.as_view(), name='list'),
    # показывает все записи блога в сжатом виде (не полност.) Может быть доступна например, по "blog/".
    url(r'^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='simple_post'),
    url(r'^archive/(?P<year>[0-9]{4})/$',  Post_YearArchiveView.as_view(),    name="Post_year_archive"), #1 pattern(s) tried: ['(<int:year>)/']
    # url(r'^comment/$', CommentForm.as_view(), name='form'),
    # url(r'^post/(?P<pk>\d+)/comment/$', CommentForm.as_view(), name='comment'),
    # Страница-архив записей – показyвает все месaца года и записи блога,   <int:year>/
    # сгруппированные по этим месяцам.
    # По умолчанию указывается date_list год, но его можно изменить на месяц или день,
    # используя атрибут date_list_period.
    ]

