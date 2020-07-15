from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns([
    path("movie/", views.MovieViewSet.as_view({'get': 'list'})),
    path("movie/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})),
    path("genre/", views.GenreViewSet.as_view({'get': 'list'})),
    path("genre/<int:pk>/", views.GenreViewSet.as_view({'get': 'retrieve'})),
    path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating/", views.RatingCreateViewSet.as_view({'post': 'create'})),
    path('actor/', views.ActorViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', views.ActorViewSet.as_view({'get': 'retrieve'})),
])
