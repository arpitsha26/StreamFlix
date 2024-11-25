from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
import uuid
from .choices import AGE_CHOICES


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=False)
    profiles=models.ManyToManyField('Profile')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

class Profile(models.Model):
    name=models.CharField(max_length=225)
    age_limit=models.CharField(max_length=5,choices=AGE_CHOICES)
    uuid=models.UUIDField(default=uuid.uuid4,unique=True)


    def __str__(self):
        return self.name +" "+self.age_limit
    
class Basemodel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    class Meta:
        abstract=True 

class Category(Basemodel):
    id = models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
class Movie(Basemodel):
    title=models.CharField(max_length=255)
    description=models.TextField()
    release_date=models.DateField()
    categories=models.ManyToManyField(Category,related_name="movies")
    poster=models.ImageField(upload_to='movie_posters/',  blank=True,null=True)
    videos=models.ManyToManyField('Video')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Series(Basemodel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name="series_categories")
    poster = models.ImageField(upload_to='series_posters/', blank=True, null=True)
    seasons = models.ManyToManyField('Season', related_name='season_series')  
    is_featured = models.BooleanField(default=False)  

    def __str__(self):
        return self.title

class Anime(Basemodel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name="anime_categories")
    poster = models.ImageField(upload_to='anime_posters/', blank=True, null=True)
    episodes = models.ManyToManyField('Episode', related_name='anime_episodes')  
    is_featured = models.BooleanField(default=False)  

    def __str__(self):
        return self.title
    
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title:str = models.CharField(max_length=225,blank=True,null=True)
    file=models.FileField(upload_to='movies')
    
class UserMovieList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_lists")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name="user_movie_lists")
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True, related_name="user_series_lists")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, null=True, blank=True, related_name="user_anime_lists")
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.movie:
            return f"{self.user.email} - Movie: {self.movie.title}"
        elif self.series:
            return f"{self.user.email} - Series: {self.series.title}"
        elif self.anime:
            return f"{self.user.email} - Anime: {self.anime.title}"
        else:
            return f"{self.user.email} - Unknown Media"

class WatchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_history")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watch_history")
    watched_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0, help_text="Progress in seconds")

    def __str__(self):
        return f"{self.user.email} watched {self.movie.title}"

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=1, help_text="Rating out of 5")
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} on {self.movie.title}"
    


class Season(Basemodel):
    series = models.ForeignKey('Series', on_delete=models.CASCADE, related_name='series_seasons')
    title = models.CharField(max_length=255)
    episodes = models.ManyToManyField('Episode', related_name='episode_seasons') 
    season_number = models.PositiveIntegerField()  
    poster = models.ImageField(upload_to='series/seasons_posters/', blank=True, null=True)  

    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}: {self.title}"


class Episode(Basemodel):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='season_episodes') 
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    file = models.FileField(upload_to='series/episodes') 
    episode_number = models.PositiveIntegerField()  

    def __str__(self):
        return f"Season {self.season.season_number}, Episode {self.episode_number}: {self.title}"





class AnimeEpisode(Basemodel):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='anime_episodes') 
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    file = models.FileField(upload_to='anime/episodes')  
    episode_number = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.anime.title} - Episode {self.episode_number}: {self.title}"