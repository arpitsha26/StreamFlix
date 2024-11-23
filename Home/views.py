from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers import RegisterSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.conf import settings
import datetime
import jwt
import json







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

    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = CustomUser.objects.get(email = email)
            if not user:
                return HttpResponse("user with this mail not found")
            if check_password(password,user.password):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1), 
                    "iat": datetime.datetime.utcnow(), 
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
                response = f"token = {token}"
                return HttpResponse(response)
            else:
                return HttpResponse("enter a valid password")
        except Exception as e:
            return HttpResponse('Error occured')

