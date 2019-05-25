# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from blog.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Post, Comment, UserAccount
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from blog.forms import CommentForm, RegistrationForm, LoginForm
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
#   from django.contrib.sessions.middleware import SessionMiddleware # add_user_session_data

User = get_user_model()

class Privet(TemplateView):
    model = Post
    template_name = "blog/home.html"
    allow_future = False

    def get_context_data(self, **kwargs):
        context = super(Privet, self).get_context_data(**kwargs)
        queryset = Post.objects.order_by('-datetime')[:6]
        context['list_home'] = [x for x in queryset]         # ','.join([x.title for x in queryset])
        context['obj'] = queryset[0]
        return context



class PostsListView(ListView):
    model = Post
    queryset = Post.objects.order_by('-datetime')
    template_name = "blog/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self,  **kwargs):  # если указать request, *args, то пишет что не находит request
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comment_list = (
            Comment.objects.filter(post=self.object).order_by('-timestamp')
        )

        # for comment in comment_list:                                #Разобраться как работает этот цикл и зачем здесь модерация
        #     comment._post_url = self.object.get_absolute_url()
        #     if not comment.moder:
        #         comment.url = ''
        #         comment.content = ('Comment is under moderation')
        #         comment.under_moderation_class = 'comment-under-moderation'

        context['comment_tree'] = comment_list             # make_tree(comment_list)


        context['comment_form'] = CommentForm()
        #     initial=add_user_session_data(self, {'post': self.object})
        # )


        context['avtor'] = Comment.user_comment
        # context['text'] = f"комментарий от {Comment.user_comment} к записи {Comment.post or Comment.parent}"
        context['comment_all'] = [x for x in comment_list]  #   [1].post.pk     # queryset
        #     if comment_form.is_valid():                           # проверка на валидацию из функции
        #         new_comment = comment_form.save(commit=False)
        #         # Assign the current post to the new comment
        #         new_comment.post = post
        #         new_comment.save()
        context['new_comment'] = None
        context['object'] = self.get_object()
        context['user_now'] = UserAccount.objects.get(user=self.request.user )


        # new_comment = None                                        # реализация  из функции
        # if request.method == 'POST':
        #     comment_form = CommentForm(data=request.POST)
        #     if comment_form.is_valid():
        #         new_comment = comment_form.save(commit=False)
        #         # Assign the current post to the new comment
        #         new_comment.post = post
        #         new_comment.save()
        # else:
        #     comment_form = CommentForm()
        # return render( request, "post_detail.html", {
        #         "post": post,
        #         "comment_form": comment_form,
        #         "new_comment": new_comment,
        #         "comments": comments,    } )
        return context


class CreateCommentView(View):
    template_name = "blog/post_detail.html"

    def post(self, request, *args, **kwargs):
        content_id = self.request.POST.get('content_id')
        comment = self.request.POST.get('comment')
        entry = Post.objects.get(id=content_id)
        new_comment = Comment.create(user_comment=request.user, post=entry, message = comment)
        comment = [{'user_comment': new_comment.user_comment.username, 'post': new_comment.post,
                    'message': new_comment.message, 'timestamp': new_comment.timestamp}]
        return JsonResponse(comment, safe=False)


class uno(View):
    template_name = "blog/index"


class Post_YearArchiveView(YearArchiveView):
    model = Post
    queryset = Post.objects.all()           # .reverse()
    date_field = "datetime"     # Сортировать по дате публикации
    make_object_list = True     # передавать в контексте список статей
    allow_future = False    # Не показывать статьи с датой публикации в будующем

    template_name = "blog/archive.html"


class Post_MonthArchiveView(MonthArchiveView):
    model = Post
    queryset = Post.objects.all()
    date_field = "datetime"     # Сортировать по дате публикации
    make_object_list = True     # передавать в контексте список статей
    allow_future = False    # Не показывать статьи с датой публикации в будующем
    template_name = "blog/month_archive.html"


class Post_DayArchiveView(DayArchiveView):
    model = Post
    queryset = Post.objects.all()
    date_field = "datetime"     # Сортировать по дате публикации
    make_object_list = True     # передавать в контексте список статей
    allow_future = False    # Не показывать статьи с датой публикации в будующем
    template_name = "blog/day_archive.html"
#
# class CreateObject(edit.CreateView):
#     model = Post
#
# class EditObject(edit.UpdateView):
#     model = Post
#
# class DeleteObject(edit.DeleteView):
#     model = Post
#     success_url = '/'

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


class UserRoom(View):

    template_name = 'blog/userroom.html'

    def get(self, request, *args, **kwargs):

        user = self.kwargs.get('user')
        user_now = UserAccount.objects.get(user=User.objects.get(username=user))
        #   user_now.favorite_posts.add(post)
        context = {
            'user_now': user_now
                }
        return render(self.request, self.template_name, context, )


# class LogOut(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'blog:home'
