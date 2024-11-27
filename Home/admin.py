from django.contrib import admin
from .models import CustomUser, UserMovieList, Movie, Category, WatchHistory, Review, Video, Genre


admin.site.register(CustomUser)
admin.site.register(UserMovieList)
admin.site.register(Movie)
admin.site.register(Category)
admin.site.register(WatchHistory)
admin.site.register(Video) 
admin.site.register(Genre) 


