from django.contrib.syndication.views import Feed
from apps.blog.models import Post

class LatestPostsFeed(Feed):
    title='Последние записи Django Blog'
    description='Новые зап Django Blog'
    link='/feeds/'


    def items(self):
        return Post.custom.order_by('-create')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

