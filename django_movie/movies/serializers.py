from rest_framework import serializers

from .models import Movie, Genre, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр отзывов, вывод только тех у кого нет parent"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Рекурсивный вывод children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorListSerializer(serializers.ModelSerializer):
    """Список актеров и режиссеров"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """Информация об актере или режиссере"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'rating_user', 'middle_star', 'poster', 'genres')


class GenreListSerializer(serializers.ModelSerializer):
    """Список жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'description',)


class GenreDetailSerializer(serializers.ModelSerializer):
    """Информация о жанре"""

    class Meta:
        model = Genre
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('id', 'name', 'text', 'children',)


class MovieDetailSerializer(serializers.ModelSerializer):
    """Информация о фильме"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class RatingCreateSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к фильму"""

    class Meta:
        model = Rating
        fields = ('star', 'movie',)

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating