from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    """Model representing a movie genre."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    """Model representing a person involved in movies (actor/director)."""
    ROLE_CHOICES = (
        ('actor', 'Actor'),
        ('director', 'Director'),
        ('both', 'Both'),
    )
    name = models.CharField(max_length=150)
    biography = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='actor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class Movie(models.Model):
    """Model representing a movie entity."""
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    release_year = models.IntegerField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    directors = models.ManyToManyField(
        Person, 
        related_name='directed_movies',
        limit_choices_to={'role__in': ['director', 'both']}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Rating(models.Model):
    """Model representing a movie review rating."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movie.title} - {self.score}/5"