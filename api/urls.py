
from django.urls import path
from Home.views import *
urlpatterns = [
    path(''),
    path('profile/'),
    path('profile/create'),
    path('watch/<str:profile_id>/'),
    path('movie/list'),
    path('movie/deatil/<str:movie_id>'),
    path('movie/play/<str:movie_id>/'),
]
