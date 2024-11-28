from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers import RegisterSerializer, MovieSerializer, MovieCreateUpdateSerializer, UserMovieListSerializer, UserProfileSerializer
from .models import CustomUser, Movie, UserMovieList
from django.contrib.auth.hashers import check_password
from django.conf import settings
import datetime
from rest_framework.permissions import IsAuthenticated
import jwt
import json
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed







class signup(APIView):
    permission_classes=[]
    authentication_classes=[]
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
    permission_classes=[]
    authentication_classes=[]
    
    def post(self, request):
            email = request.data['email']
            password = request.data['password']
            try:
                user = CustomUser.objects.get(email=email)
                if check_password(password, user.password):
                    payload = {
                        "id": user.id,
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
    permission_classes=[]
    authentication_classes=[]
    
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
    

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(id=payload["id"])
            return (user, None)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
            return None




class mylist(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_movie_list = UserMovieList.objects.filter(user=request.user)
        serializer = UserMovieListSerializer(user_movie_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        movie_id = request.data.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        
        if UserMovieList.objects.filter(user=request.user, movie=movie).exists():
            return Response({'detail': 'Movie is already in your list.'}, status=status.HTTP_400_BAD_REQUEST)

        UserMovieList.objects.create(user=request.user, movie=movie)
        return Response({'detail': 'Movie added to your list.'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        movie_id = request.data.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
       
        user_movie_list = UserMovieList.objects.filter(user=request.user, movie=movie).first()

        if not user_movie_list:
            return Response({'detail': 'Movie not found in your list.'}, status=status.HTTP_404_NOT_FOUND)

        user_movie_list.delete()
        return Response({'detail': 'Movie removed from your list.'}, status=status.HTTP_204_NO_CONTENT)


class UserProfile(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user 
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user   
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

