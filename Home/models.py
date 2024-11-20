from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
import uuid
from .choices import AGE_CHOICES


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    profiles=models.ManyToManyField('Profile')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(models.Model):
    name=models.CharField(max_length=225)
    age_limit=models.CharField(max_length=5,choices=AGE_CHOICES)
    uuid=models.UUIDField(default=uuid.uuid4,unique=True)


    def __str__(self):
        return self.name +" "+self.age_limit
    
class Basemodel(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    class Meta:
        abstract=True 

class Category(Basemodel):
    category_name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Movie(Basemodel):
    title=models.CharField(max_length=255)
    description=models.TextField()
    release_date=models.DateField()
    categories=models.ManyToManyField(Category,related_name="movies")
    poster=models.models.ImageField(upload_to='movie_posters/',  blank=True,null=True)
    videos=models.ManyToManyField('Video')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Video(models.Model):
    title:str = models.CharField(max_length=225,blank=True,null=True)
    file=models.FileField(upload_to='movies')
    
class UserMovieList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="movie_lists")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="user_lists")
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.movie.title}"

class WatchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="watch_history")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watch_history")
    watched_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0, help_text="Progress in seconds")

    def __str__(self):
        return f"{self.user.email} watched {self.movie.title}"

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=1, help_text="Rating out of 5")
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} on {self.movie.title}"
    