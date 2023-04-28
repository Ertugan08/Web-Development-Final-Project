from django.urls import path
from api.views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('category/', CategoryAPIListView.as_view()),
    path('home/', EventAPIListView.as_view()),
    path('home/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view()),
    path('category/<int:pk>/', CategoryItemsAPIView.as_view()),
    path('favorites/', FavoritesAPIView.as_view()),
    path('like/<int:pk>/', like)
]