from django.shortcuts import render
from django.db.models import Avg
from .models import Movie, Genre


def movie_recommendations(request):
    """
    Public view showing top-rated movies per genre.
    Contrasts administrative panel features with custom client UI.
    """
    genre_id = request.GET.get('genre')
    movies = Movie.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')

    if genre_id:
        movies = movies.filter(genres__id=genre_id)

    genres = Genre.objects.all()

    context = {
        'movies': movies[:5],
        'genres': genres,
        'selected_genre': genre_id
    }
    return render(request, 'movies/recommendations.html', context)