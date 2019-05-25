# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    user_post = models.ForeignKey(User,  on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=255, default='')
    datetime = models.DateTimeField('Дата публикации') # время каждого сохранения, изменения
    content = models.TextField('Содержание', default='')
    pub_date = models.DateField(auto_now_add=True) #время первой публикации
    moder = models.BooleanField("Модерация", default=False)

    def get_absolute_url(self):
        return f"/post/{self.pk}/"

    # class Meta:
    #     ordering = ('-datetime')

class Comment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=('коментируемая статья'))
    parent = models.ForeignKey('self', default=0, blank=True, null=True,  on_delete=models.DO_NOTHING)  #related_name='ответ на',

    message = models.TextField(max_length=1500, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    moder = models.BooleanField("Модерация", default=False)


    class Meta:
        ordering = ("-timestamp",)

    # def __str__(self):
    #     return f"комментарий от {User} к записи {self.post or self.parent}"

class UserAccount(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, default=None, blank=True, null=True )
    last_name = models.CharField(max_length=200, default=None, blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    faivorite_post = models.ManyToManyField(Post)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('account_view', kwargs={'user':self.user.username})