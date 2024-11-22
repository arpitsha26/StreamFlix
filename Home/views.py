
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers import RegisterSerializer

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


