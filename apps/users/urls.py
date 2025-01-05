from django.urls import path
from .views import *

urlpatterns = [
    # Position endpoints
    path('positions/', PositionsListCreateAPIView.as_view(), name='position-list-create'),
    path('positions/<int:pk>/', PositionRetrieveUpdateDestroyAPIView.as_view(), name='position-retrieve-update-destroy'),
    # User endpoints
    # path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    # Doctors endpoints
    path('doctors/', DoctorCreateView.as_view(), name='doctor-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    # Nurses endpoints
    path('nurse/', DoctorCreateView.as_view(), name='doctor-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
]