from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Article, Category


def published_articles():
    return Article.objects.filter(
        published_at__lte=timezone.now()
    ).select_related('author').prefetch_related('categories')


def home(request):
    return render(request, 'news/home.html', {
        'articles': published_articles(), 'categories': Category.objects.all(),
    })


def detail(request, slug):
    article = get_object_or_404(published_articles(), slug=slug)
    return render(request, 'news/detail.html', {
        'article': article, 'categories': Category.objects.all(),
    })


def category(request, slug):
    selected_category = get_object_or_404(Category, slug=slug)
    return render(request, 'news/category.html', {
        'category': selected_category,
        'articles': published_articles().filter(categories=selected_category),
        'categories': Category.objects.all(),
    })
