from django.db import models

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Genre, Actor

from .serializers import MovieListSerializer, MovieDetailSerializer
from .serializers import GenreListSerializer, GenreDetailSerializer
from .serializers import ReviewCreateSerializer
from .serializers import RatingCreateSerializer
from .serializers import ActorListSerializer, ActorDetailSerializer

from .service import get_client_ip
from .service import MovieFilter
from .service import MoviePagination


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = MoviePagination

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request))),
            middle_star=models.Avg('ratings__star'),
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        elif self.action == 'retrieve':
            return GenreDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class RatingCreateViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer
