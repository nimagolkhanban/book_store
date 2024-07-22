from django.db import connection
from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer


# class UserRegistrationView(APIView):
#     def post(self, request):
#         # we pass in the data arg because we need to check that data is valid or not
#         serializer = UserRegistrationSerializer(data=request.POST)
#         if serializer.is_valid():
#             User.objects.create_user(
#                 username=serializer.validated_data['username'],
#                 email=serializer.validated_data['email'],
#                 password=serializer.validated_data['password']
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    def post(self, request):
        # Check if data is valid
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Insert user into database
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO auth_user (username, email, password)
                    VALUES (%s, %s, %s)
                """, [username, email, password])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)