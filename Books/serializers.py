from rest_framework.serializers import ModelSerializer

from Books.models import Book


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id']

