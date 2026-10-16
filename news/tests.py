from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Author, Category


class PortalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(name='Test author')
        cls.category = Category.objects.create(name='Cine', slug='cine')
        cls.article = Article.objects.create(
            title='Una noticia', slug='una-noticia', summary='Resumen editorial',
            body='<script>alert("test")</script>', author=cls.author,
            published_at=timezone.now() - timedelta(days=1),
        )
        cls.article.categories.add(cls.category)
        cls.future = Article.objects.create(
            title='Future article', slug='future', summary='Future', body='Future',
            author=cls.author, published_at=timezone.now() + timedelta(days=1),
        )

    def test_home_reuses_card_and_hides_future_articles(self):
        response = self.client.get(reverse('news:home'))
        self.assertContains(response, 'Una noticia')
        self.assertNotContains(response, 'Future article')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'news/_article_card.html')

    def test_detail_escapes_stored_html(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_category_filters_and_reuses_card(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertContains(response, self.article.title)
        self.assertTemplateUsed(response, 'news/_article_card.html')
        other = Category.objects.create(name='Otra', slug='otra')
        response = self.client.get(other.get_absolute_url())
        self.assertNotContains(response, self.article.title)
        self.assertContains(response, 'Todavía no hay noticias')

    def test_missing_and_future_pages_return_404(self):
        for url in [self.future.get_absolute_url(), reverse('news:detail', args=['missing']),
                    reverse('news:category', args=['missing'])]:
            self.assertEqual(self.client.get(url).status_code, 404)

    def test_admin_edits_are_reflected_in_portal(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser('reviewer', password='test-only-password')
        self.client.force_login(user)
        response = self.client.post(reverse('admin:news_article_change', args=[self.article.pk]), {
            'title': 'Título actualizado', 'slug': self.article.slug,
            'summary': self.article.summary, 'body': self.article.body,
            'author': self.author.pk, 'categories': [self.category.pk],
            'published_at_0': '2026-01-01', 'published_at_1': '10:00:00', '_save': 'Guardar',
        })
        self.assertEqual(response.status_code, 302)
        self.assertContains(self.client.get(self.article.get_absolute_url()), 'Título actualizado')

    def test_previous_lab_page_still_renders(self):
        self.assertEqual(self.client.get(reverse('recommendations')).status_code, 200)
