from django.urls import path
from .views import *

urlpatterns = [
    # User endpoints
    path('users/get-me/', UserProfile.as_view(), name='user-profile'),
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
    path('users/update-password/', PasswordUpdateView.as_view(), name='update-password'),
    # Doctors endpoints
    # path('doctors/', DoctorCreateView.as_view(), name='doctor-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-retrieve-update-destroy'),
]