from .models import Movie

class MovieServices:

    @staticmethod
    def get_movies():
        return Movie.objects.all()

    @staticmethod
    def search_by_title(title):
        return Movie.objects.filter(title__icontains=title)

    @staticmethod
    def create_movie(data):
        return Movie.objects.create(
            title = data["title"],
            director = data["director"],
            genre = data["genre"],
            duration_minutes = data["duration_minutes"]
        )