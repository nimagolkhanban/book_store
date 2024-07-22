from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.AddReviewsView.as_view(), name='add-review'),
    path('update/', views.UpdateReviewView.as_view(), name='update-review'),
    path('delete/', views.DeleteReviewView.as_view(), name='delete-review'),
]