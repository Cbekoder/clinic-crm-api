from django.urls import path
from .views import *

urlpatterns = [
    # Position endpoints
    # path('positions/', PositionListCreateAPIView.as_view(), name='position-list-create'),
    path('positions-doctor/', DoctorPositions.as_view(), name='doctor_positions'),
    path('positions-nurse/', NursePositions.as_view(), name='nurse_positions'),
    path('positions-other/', OtherPositions.as_view(), name='other_positions'),
    path('position/<int:pk>/', PositionRetrieveUpdateDestroyAPIView.as_view(), name='position-retrieve-update-destroy'),
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