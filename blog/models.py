from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField('Дата публикации') # время каждого сохранения, изменения
    content = models.TextField()
    pub_date = models.DateField(auto_now_add=True) #время первой публикации


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%i/" % self.id

class Comment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1500)
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', default=0, blank=True, null=True, related_name='parent_comment', on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"комментарий от {User} к записи {self.post or self.parent}"


