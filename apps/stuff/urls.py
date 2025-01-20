from django.urls import path
from .views import (
    SectionListCreateAPIView, SectionRetrieveUpdateDestroyAPIView,
    RoomListCreateAPIView, RoomRetrieveUpdateDestroyAPIView, ServiceListCreateView, ServiceDetailView,
    ExpensesListCreateView, ExpenseDetailView
)

urlpatterns = [
    # Section URLs
    path('sections/', SectionListCreateAPIView.as_view(), name='section-list-create'),
    path('sections/<int:pk>/', SectionRetrieveUpdateDestroyAPIView.as_view(), name='section-detail'),

    # Room URLs
    path('rooms/', RoomListCreateAPIView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomRetrieveUpdateDestroyAPIView.as_view(), name='room-detail'),

    # Service URLs
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    # Expense URLs
    path('expenses/', ExpensesListCreateView.as_view(), name='expenses-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expenses-detail'),
]
