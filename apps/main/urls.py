from django.urls import path
from .views import PatientListCreateAPIView, TurnListCreateAPIView, TurnRetrieveUpdateDestroyAPIView, TurnCancelAPIView, \
    ClientListCreateAPIView, PatientRetrieveUpdateDestroyAPIView, PatientServiceRetrieveUpdateDestroyAPIView, \
    PatientServiceListCreateAPIView, ClientRetrieveUpdateDestroyAPIView, DoctorTurnUpdateAPIView

urlpatterns = [
    # Client urls
    path('clients/', ClientListCreateAPIView.as_view(), name='patient_list_create'),
    path('clients/<int:pk>', ClientRetrieveUpdateDestroyAPIView.as_view(), name='patient-detail'),

    # Turn urls
    path('turns/', TurnListCreateAPIView.as_view(), name='turn-list-create'),
    path('turns/<int:id>', TurnRetrieveUpdateDestroyAPIView.as_view(), name='turn-detail-update-delete'),
    path('turns/doctor/<int:pk>', DoctorTurnUpdateAPIView.as_view(), name='doctor-turn-update'),
    path('turns/cancel/<int:pk>', TurnCancelAPIView.as_view(), name='turn-cancel'),

    # Pateint urls
    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyAPIView.as_view(), name='patient-detail'),

    # PatientService URLs
    path('patient-services/', PatientServiceListCreateAPIView.as_view(), name='patient-service-list-create'),
    path('patient-services/<int:pk>/', PatientServiceRetrieveUpdateDestroyAPIView.as_view(),
         name='patient-service-detail'),

]
