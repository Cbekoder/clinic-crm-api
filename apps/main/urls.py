from django.urls import path
from .views import PatientListCreateAPIView, TurnListCreateAPIView, TurnRetrieveUpdateDestroyAPIView, TurnCancelAPIView

urlpatterns = [
    path('patients/', PatientListCreateAPIView.as_view(), name='patient_list_create'),
    path('turns/', TurnListCreateAPIView.as_view(), name='turn-list-create'),
    path('turn/<int:id>', TurnRetrieveUpdateDestroyAPIView.as_view(), name='turn-detail-update-delete'),
    path('turn-cancel/<int:pk>', TurnCancelAPIView.as_view(), name='turn-cancel'),
]
