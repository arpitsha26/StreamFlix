from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers import RegisterSerializer, MovieSerializer, MovieCreateUpdateSerializer
from .models import CustomUser, Movie
from django.contrib.auth.hashers import check_password
from django.conf import settings
import datetime
from rest_framework.permissions import IsAuthenticated
import jwt
import json
from rest_framework.authentication import TokenAuthentication







class signup(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"error": "error undef..", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class login(APIView):
 def post(self, request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = CustomUser.objects.get(email=email)
            if check_password(password, user.password):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                    "iat": datetime.datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
                return Response({"token": token})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class movielist(APIView):
    
    def get(self, request):
        movies = Movie.objects.all().order_by('-release_date')
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.save()
            if 'categories' in request.data:
                movie.categories.set(request.data['categories'])
            if 'videos' in request.data:
                movie.videos.set(request.data['videos'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)