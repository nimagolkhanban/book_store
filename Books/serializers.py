from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from Reviews.models import Review
from Books.models import Book


class BookSerializer(ModelSerializer):
    user_rate = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id']

    def get_user_rate(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                review = Review.objects.get(user=request.user, book=obj)
                return review.rating
            except Review.DoesNotExist:
                return None
        return None

