from django import template
from blog.models import Post
from django.db.models import Count
register=template.Library()


@register.simple_tag()
def total_posts():
    return Post.publish.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(post_count=5):
    latest_posts=Post.publish.order_by('-published')[:post_count]
    return {'latest_posts':latest_posts}

@register.simple_tag()
def get_most_commented_posts(count=5):
    return Post.publish.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]