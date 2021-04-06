from testApp.models import Post
from django import template
register=template.Library()


@register.simple_tag
def total_post():
    return Post.objects.count()


@register.inclusion_tag('testApp/latest_posts123.html')
def show_latest_post(count=5):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}


from django.db.models import Count
@register.simple_tag
def get_most_commented_posts(count=4):
    return Post.objects.annotate(total_comment=Count('comments')).order_by('-total_comment')[:count]
