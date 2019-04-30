from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Post, Comment
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import YearArchiveView
from blog import forms


class Privet(TemplateView):
    model = Post
    template_name = "blog/home.html"
    def home(self):
        list_home = Post.objects.order_by('-pub_date')[:10]
        output = ','.join([x.title for x in list_home])
        return HttpResponse(output)


class PostsListView(ListView):
    model = Post
    template_name = "blog/post_list.html"


class PostDetailView(DetailView):
    model = Post
#    def comment_form(self, Post, ):


# class MyView(FormView):
#     form_class = MyForm
#     template_name = 'form.html'
#     success_url = '/success/'
#
#     def form_valid(self, form):
#         form.save()
#         return super(MyView, self).form_valid(form)




class Post_YearArchiveView(YearArchiveView):
    queryset = Post.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True
    template_name = "post_archive.html"

#
# class CreateObject(edit.CreateView):
#     model = Post
#
# class EditObject(edit.UpdateView):
#     model = Post
#
# class DeleteObject(edit.DeleteView):
#     model = MyModel
#     success_url = '/'

