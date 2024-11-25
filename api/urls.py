
from django.urls import path
from Home.views import signup, login, movielist, animeList, seriesList,profile
urlpatterns = [
    path('signup/', signup.as_view(), name="signup"),
    path('login/', login.as_view(), name="login"), 
    path('movies/', movielist.as_view(), name="list movies"),
    path('anime/', animeList.as_view(), name="animelist"),
    path('series/', seriesList.as_view(), name="serieslist"),
    path('profile/', profile.as_view(), name="profile"),
    

]
