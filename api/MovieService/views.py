from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Movie
from .services import MovieServices
from .serializers import MovieSerializer

class MovieListView(APIView):
    def get(self, request):
        title = request.query_params.get("title")

        if title:
            movies = MovieServices.search_by_title(title)
        else:
            movies = MovieServices.get_movies()

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        movie = MovieServices.create_movie(serializer.validated_data)
        return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
