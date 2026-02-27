from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article


class ArticleFeed(Feed):
    title = "Brückentech Articles"
    link = "/articles/"
    description = "Latest articles from Brückentech"

    def items(self):
        return Article.objects.filter(published=True).order_by('-published_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.body[:200]

    def item_link(self, item):
        return reverse('article_detail', args=[item.slug])
