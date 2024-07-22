from django.db import connection
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Reviews.models import Review
from Reviews.serializers import ReviewSerializer


# class AddReviewsView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddReviewsView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book')
        rating = request.data.get('rating')

        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not book_id or not rating:
            return Response({"detail": "Book ID and rating are required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            # Check if the review already exists
            cursor.execute("""
                SELECT id FROM "Reviews_review" 
                WHERE user_id = %s AND book_id = %s
            """, [user.id, book_id])

            existing_review = cursor.fetchone()

            if existing_review:
                return Response({"detail": "Review already exists for this book by the user."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Insert new review
            cursor.execute("""
                INSERT INTO "Reviews_review" (user_id, book_id, rating) 
                VALUES (%s, %s, %s)
            """, [user.id, book_id, rating])

        return Response({"message": "Review added successfully."}, status=status.HTTP_201_CREATED)


# class UpdateReviewView(APIView):
#     def put(self, request, *args, **kwargs):
#         try:
#             review = Review.objects.get(user=request.user, book=request.data['book'])
#         except Review.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         serializer = ReviewSerializer(review, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateReviewView(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book')
        rating = request.data.get('rating')

        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not book_id:
            return Response({"detail": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            # Check if the review exists
            cursor.execute("""
                SELECT id FROM "Reviews_review" 
                WHERE user_id = %s AND book_id = %s
            """, [user.id, book_id])

            review = cursor.fetchone()

            if not review:
                return Response(status=status.HTTP_404_NOT_FOUND)

            review_id = review[0]

            # Update the review
            cursor.execute("""
                UPDATE "Reviews_review" 
                SET rating = %s 
                WHERE id = %s
            """, [rating, review_id])

        return Response({"message": "Review updated successfully."}, status=status.HTTP_200_OK)

# class DeleteReviewView(APIView):
#     def delete(self, request, *args, **kwargs):
#         try:
#             review = Review.objects.get(user=request.user, book=request.data['book'])
#             review.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Review.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteReviewView(APIView):
    def delete(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book')

        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not book_id:
            return Response({"detail": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 1 FROM "Reviews_review" 
                WHERE user_id = %s AND book_id = %s
            """, [user.id, book_id])

            if not cursor.fetchone():
                return Response(status=status.HTTP_404_NOT_FOUND)

            # Delete the review
            cursor.execute("""
                DELETE FROM "Reviews_review" 
                WHERE user_id = %s AND book_id = %s
            """, [user.id, book_id])

        return Response(status=status.HTTP_204_NO_CONTENT)