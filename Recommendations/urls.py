from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookRecommendationView.as_view(), name='book_recommendation')
]