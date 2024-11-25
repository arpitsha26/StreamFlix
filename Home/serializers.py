from .models import CustomUser, Profile, Category, Video, Movie, UserMovieList, Review, WatchHistory, Anime, Season, Episode, Series, AnimeEpisode
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'is_verified']
        read_only_fields = ['id', 'is_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password'],
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'age_limit', 'uuid']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', ]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'file']

class MovieSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date',
            'categories', 'poster', 'videos', 'duration',
            'is_featured', 
        ]


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_date', 'categories',
            'poster', 'videos', 'duration', 'is_featured'
        ]


class UserMovieListSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source="movie.title")  
    series_title = serializers.ReadOnlyField(source="series.title")  
    anime_title = serializers.ReadOnlyField(source="anime.title") 
    user_email = serializers.ReadOnlyField(source="user.email")   

    class Meta:
        model = UserMovieList
        fields = ['id', 'user', 'user_email', 'movie', 'movie_title', 'series', 'series_title', 'anime', 'anime_title', 'added_on']
    
    def validate(self, attrs):

        if not any([attrs.get('movie'), attrs.get('series'), attrs.get('anime')]):
            raise serializers.ValidationError('At least one of movie, series, or anime must be provided.')
        if sum([bool(attrs.get('movie')), bool(attrs.get('series')), bool(attrs.get('anime'))]) > 1:
            raise serializers.ValidationError('Only one of movie, series, or anime can be added at a time.')
        return attrs


class WatchHistorySerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'movie', 'watched_at', 'progress']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'comment', 'created_at']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'duration', 'file', 'episode_number', 'created_at', 'updated_at']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Season
        fields = [
            'id',
            'title',
            'season_number',
            'episodes',
            'poster',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        episodes_data = validated_data.pop('episodes', [])
        season = Season.objects.create(**validated_data)
        for episode_data in episodes_data:
            Episode.objects.create(**episode_data, season=season)
        return season


class SeriesSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    seasons = SeasonSerializer(many=True)

    class Meta:
        model = Series
        fields = [
            'id', 
            'title', 
            'description', 
            'release_date', 
            'categories', 
            'poster', 
            'seasons', 
            'is_featured',
            'created_at', 
            'updated_at'
        ]

    def create(self, validated_data):
        seasons_data = validated_data.pop('seasons', [])
        categories = validated_data.pop('categories', [])
        series = Series.objects.create(**validated_data)
        series.categories.set(categories)
        
        for season_data in seasons_data:
            episodes_data = season_data.pop('episodes', [])
            season = Season.objects.create(series=series, **season_data)
            for episode_data in episodes_data:
                Episode.objects.create(season=season, **episode_data)
        
        return series


class AnimeEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeEpisode
        fields = ['id', 'title', 'duration', 'file', 'episode_number', 'created_at', 'updated_at']


class AnimeSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    episodes = AnimeEpisodeSerializer(many=True)

    class Meta:
        model = Anime
        fields = [
            'id', 
            'title', 
            'description', 
            'release_date', 
            'categories', 
            'poster', 
            'episodes', 
            'is_featured',
            'created_at', 
            'updated_at'
        ]

    def create(self, validated_data):
        episodes_data = validated_data.pop('episodes', [])
        categories = validated_data.pop('categories', [])
        anime = Anime.objects.create(**validated_data)
        anime.categories.set(categories)
        
        for episode_data in episodes_data:
            AnimeEpisode.objects.create(anime=anime, **episode_data)
        
        return anime