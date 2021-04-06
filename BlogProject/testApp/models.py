from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

class CustManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')
# Create your models here.
class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('published','Published'))
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique_for_date='publish')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects=CustManager()
    tags=TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):  #anywhere to want to display this post object use self.title
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,
                       self.publish.strftime('%m'),
                       self.publish.strftime('%d'),self.slug])

#comments implementation
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=100)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return "Commented By {} on {}".format(self.name,self.post)
