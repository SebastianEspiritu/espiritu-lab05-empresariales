from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news:category', args=[self.slug])


class Author(models.Model):
    name = models.CharField(max_length=150)
    biography = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    body = models.TextField()
    featured_image = models.ImageField(upload_to='news/', blank=True)
    image_description = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='articles')
    categories = models.ManyToManyField(Category, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', args=[self.slug])
