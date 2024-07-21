from django.contrib.auth.models import User
from django.db import models
from Books.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} rated {self.rating} to {self.book}'
