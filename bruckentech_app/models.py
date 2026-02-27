from django.db import models
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from markdown import markdown


class Article(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	excerpt = models.TextField(blank=True)
	body = models.TextField(help_text="Write article body in Markdown")
	image = models.ImageField(upload_to='articles/%Y/%m/%d/', blank=True, null=True)
	published = models.BooleanField(default=False)
	published_at = models.DateTimeField(blank=True, null=True)
	author = models.CharField(max_length=128, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-published_at", "-created_at"]

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)[:255]
		super().save(*args, **kwargs)

	@property
	def body_html(self):
		"""Render Markdown body to safe HTML for templates."""
		return mark_safe(markdown(self.body or "", extensions=["extra", "sane_lists"]))

