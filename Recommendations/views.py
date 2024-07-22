from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


class BookRecommendationView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        recommendations = {
            "genre_based": self.get_genre_based_recommendations(user),
            "author_based": self.get_author_based_recommendations(user),
            "similar_user_based": self.get_similar_user_based_recommendations(user)
        }

        return Response(data=recommendations, status=status.HTTP_200_OK)

    def get_genre_based_recommendations(self, user):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH UserGenreRatings AS (
                    SELECT genre, AVG(rating) AS avg_rating
                    FROM "Reviews_review"
                    JOIN "Books_book" ON "Reviews_review".book_id = "Books_book".id
                    WHERE user_id = %s
                    GROUP BY genre
                )
                SELECT genre FROM UserGenreRatings
                ORDER BY avg_rating DESC
                LIMIT 1
            """, [user.id])
            favorite_genre = cursor.fetchone()

            if not favorite_genre:
                return {"message": "Not enough data to determine favorite genre.", "books": []}

            favorite_genre = favorite_genre[0]

            cursor.execute("""
                SELECT * FROM "Books_book"
                WHERE genre = %s
                AND id NOT IN (
                    SELECT book_id FROM "Reviews_review" WHERE user_id = %s
                )
            """, [favorite_genre, user.id])

            books = cursor.fetchall()
            book_list = [
                {
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "genre": row[3]
                } for row in books
            ]

        return {
            "message": f"Books in your favorite genre '{favorite_genre}' that you haven't rated yet.",
            "books": book_list
        }

    def get_author_based_recommendations(self, user):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH HighRatedBooks AS (
                    SELECT "Books_book".author
                    FROM "Reviews_review"
                    JOIN "Books_book" ON "Reviews_review".book_id = "Books_book".id
                    WHERE user_id = %s AND rating >= 4
                    GROUP BY "Books_book".author
                )
                SELECT DISTINCT author FROM HighRatedBooks
            """, [user.id])
            authors = cursor.fetchall()

            if not authors:
                return {"message": "Not enough data to determine preferred authors.", "books": []}

            authors = [author[0] for author in authors]

            cursor.execute("""
                SELECT * FROM "Books_book"
                WHERE author IN %s
                AND id NOT IN (
                    SELECT book_id FROM "Reviews_review" WHERE user_id = %s
                )
            """, [tuple(authors), user.id])

            books = cursor.fetchall()
            book_list = [
                {
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "genre": row[3]
                } for row in books
            ]

        return {
            "message": "Books by authors you have rated highly but haven't rated yourself.",
            "books": book_list
        }

    def get_similar_user_based_recommendations(self, user):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH UserRatings AS (
                    SELECT book_id, rating
                    FROM "Reviews_review"
                    WHERE user_id = %s
                ),
                SimilarUsers AS (
                    SELECT r2.user_id
                    FROM "Reviews_review" r1
                    JOIN "Reviews_review" r2 ON r1.book_id = r2.book_id AND r1.rating = r2.rating
                    WHERE r1.user_id = %s
                    GROUP BY r2.user_id
                    HAVING COUNT(DISTINCT r1.book_id) > 5
                )
                SELECT DISTINCT r1.book_id
                FROM "Reviews_review" r1
                JOIN SimilarUsers s ON r1.user_id = s.user_id
                LEFT JOIN "Reviews_review" r2 ON r1.book_id = r2.book_id AND r2.user_id = %s
                WHERE r2.book_id IS NULL AND r1.rating >= 4
            """, [user.id, user.id, user.id])

            recommended_books = cursor.fetchall()
            book_list = [
                {
                    "id": row[0],
                    "title": row[1],
                    "author": row[2],
                    "genre": row[3]
                } for row in recommended_books
            ]

        if not book_list:
            return {"message": "Not enough data to provide recommendations based on similar users.", "books": []}

        return {
            "message": "Books that similar users rated highly but you haven't rated yet.",
            "books": book_list
        }