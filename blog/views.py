# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from django.contrib.auth import get_user_model, authenticate, login
from blog.urls import *
from blog.models import Post, Comment, UserAccount
from blog.forms import CommentForm, RegistrationForm, LoginForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


User = get_user_model()

class Privet(TemplateView):
    model = Post
    template_name = "blog/home.html"
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super(Privet, self).get_context_data(**kwargs)
        queryset = Post.objects.order_by('-datetime')[:10]
        context['list_home'] = [x for x in queryset]
        return context


class PostsListView(ListView):
    model = Post
    queryset = Post.objects.order_by('-datetime')
    template_name = "blog/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self,  **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comment_list = (
                            Comment.objects.filter(post=self.object).order_by('-timestamp')
                        )
        context['comment_tree'] = comment_list
        context['comment_form'] = CommentForm()
        context['avtor'] = Comment.user_comment
        context['comment_all'] = [x for x in comment_list]
        context['new_comment'] = None
        context['object'] = self.get_object()
        return context


class Post_YearArchiveView(YearArchiveView):
    model = Post
    queryset = Post.objects.all()
    date_field = "datetime"     # Сортировать по дате публикации
    make_object_list = True     # передавать в контексте список статей
    allow_future = False    # Не показывать статьи с датой публикации в будующем

    template_name = "blog/archive.html"


class Post_MonthArchiveView(MonthArchiveView):
    model = Post
    queryset = Post.objects.all()
    date_field = "datetime"
    make_object_list = True
    allow_future = False
    template_name = "blog/month_archive.html"


class Post_DayArchiveView(DayArchiveView):
    model = Post
    queryset = Post.objects.all()
    date_field = "datetime"
    make_object_list = True
    allow_future = False
    template_name = "blog/day_archive.html"



class RegistrationView(View):
    template_name = 'blog/registration.html'

    def get(self, request, *args, **kwargs):

        form = RegistrationForm(request.POST or None)
        context = {
           "form": form
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_user.set_password(password)
            password_check = form.cleaned_data['password_check']
            new_user.save()
            UserAccount.objects.create(user=User.objects.get(username=new_user.username),
                                       first_name=new_user.first_name,
                                       last_name=new_user.last_name,
                                       email=new_user.email)
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(self.request, self.template_name, context)

class LoginView(View):
    template_name = 'blog/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            "form": form
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(self.request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(self.request, self.template_name, context)



class post_Create(PermissionRequiredMixin, CreateView):
    permission_required = 'can_create'
    model = Post
    fields = '__all__'


class PostUpdate(UpdateView):
    model = Post
    fields = ['user_post','datetime','moder']

class PostDelete(DeleteView):
    permission_required = 'can_delete'
    model = Post
    success_url = reverse_lazy('home')