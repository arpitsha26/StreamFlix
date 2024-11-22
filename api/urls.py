
from django.urls import path
from Home.views import signup
urlpatterns = [
    path('signup/', signup.as_view(), name="signup"),

]
