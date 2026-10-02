from django.contrib import admin
from .models import Genre, Person, Movie, Rating


class RatingInline(admin.TabularInline):
    """Inline rating management inside Movie form."""
    model = Rating
    extra = 1
    readonly_fields = ('created_at', 'updated_at')  # Step 7


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')  # Step 7


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'created_at')
    list_filter = ('role',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')  # Step 7


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_year', 'display_genres', 'created_at')  # Step 5
    list_filter = ('genres', 'release_year')  # Step 5
    search_fields = ('title',)  # Step 5
    inlines = [RatingInline]  # Step 6
    readonly_fields = ('created_at', 'updated_at')  # Step 7

    @admin.display(description='Genres')
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'score', 'created_at')
    list_filter = ('score', 'movie__genres')
    search_fields = ('movie__title', 'comment')
    readonly_fields = ('created_at', 'updated_at')  # Step 7