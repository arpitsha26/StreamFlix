from django.contrib import admin
from .models import CustomUser, UserMovieList, Profile, Movie, Category, WatchHistory, Review, Video


admin.site.register(CustomUser)
admin.site.register(UserMovieList)
admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(WatchHistory)
admin.site.register(Review) 
admin.site.register(Video)
