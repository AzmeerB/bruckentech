from django.contrib import admin
from .models import Article
from markdownx.admin import MarkdownxModelAdmin


@admin.register(Article)
class ArticleAdmin(MarkdownxModelAdmin, admin.ModelAdmin):
	list_display = ("title", "author", "published", "published_at", "created_at", "image_tag")
	list_filter = ("published",)
	search_fields = ("title", "excerpt", "body", "author")
	prepopulated_fields = {"slug": ("title",)}
	readonly_fields = ("created_at", "updated_at")

	def image_tag(self, obj):
		if obj.image:
			from django.utils.html import format_html
			return format_html('<img src="{}" style="max-width:100px; height:auto;" />', obj.image.url)
		return ""

	image_tag.short_description = 'Image'
