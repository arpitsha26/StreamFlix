
from django.urls import path
from Home.views import signup, login, movielist, mylist, UserProfile
urlpatterns = [
    path('signup/', signup.as_view(), name="signup"),
    path('login/', login.as_view(), name="login"), 
    path('movies/', movielist.as_view(), name="list movies"),
    path('mylist/', mylist.as_view(), name='userlist'),
    path('profile/', UserProfile.as_view(), name="user profile"),

]
