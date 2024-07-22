from django.db import connection
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from Books.models import Book
from Books.serializers import BookSerializer


# class BookListView(APIView):
#     def get(self, request):
#         genre = request.query_params.get('genre')
#         if genre:
#             books = Book.objects.filter(genre=genre)
#         else:
#             books = Book.objects.all()
#         serializer_data = BookSerializer(books, many=True, context={'request': request})
#         return Response(data=serializer_data.data, status=status.HTTP_200_OK)

class BookListView(APIView):
    def get(self, request):
        genre = request.query_params.get('genre')
        user_id = request.user.id if request.user.is_authenticated else None

        with connection.cursor() as cursor:
            if genre:
                cursor.execute('SELECT * FROM "Books_book" WHERE genre = %s', [genre])
            else:
                cursor.execute('SELECT * FROM "Books_book"')

            books = cursor.fetchall()

            if user_id:
                cursor.execute('''
                    SELECT book_id, rating
                    FROM "Reviews_review"
                    WHERE user_id = %s
                ''', [user_id])
                user_ratings = cursor.fetchall()
                user_rating_dict = {book_id: rating for book_id, rating in user_ratings}
            else:
                user_rating_dict = {}

            book_list = [
                {
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "genre": row[3],
                    "user_rate": user_rating_dict.get(row[0], None)
                } for row in books
            ]

        return Response(data=book_list, status=status.HTTP_200_OK)


