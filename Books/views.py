from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from Books.models import Book
from Books.serializers import BookSerializer


class BookListView(APIView):
    def get(self, request):
        genre = request.query_params.get('genre')
        if genre:
            books = Book.objects.filter(genre=genre)
        else:
            books = Book.objects.all()
        serializer_data = BookSerializer(books, many=True)
        return Response(data=serializer_data.data, status=status.HTTP_200_OK)





