from django.urls import path
from Books import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),

]