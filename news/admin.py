from django.contrib import admin

from .models import Article, Author, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'biography')
    list_filter = ('name',)
    search_fields = ('name', 'biography')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'updated_at')
    list_filter = ('categories', 'author', 'published_at')
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'published_at'


admin.site.site_header = 'Espíritu · Administración'
admin.site.site_title = 'Espíritu'
