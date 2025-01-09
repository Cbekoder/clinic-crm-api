from django.urls import path
from .views import PatientListCreateAPIView, TurnListCreateAPIView, TurnRetrieveUpdateDestroyAPIView, TurnCancelAPIView, \
    ClientListCreateAPIView, PatientRetrieveUpdateDestroyAPIView, PatientServiceRetrieveUpdateDestroyAPIView, \
    PatientServiceListCreateAPIView, ClientRetrieveUpdateDestroyAPIView, DoctorTurnUpdateAPIView, \
    PatientPaymentListCreateAPIView, PatientPaymentRetrieveUpdateDestroyAPIView, TurnFullDetailAPIView, ReportView, \
    DoctorTurnListAPIView, TurnFullDetailRetrieveAPIView

urlpatterns = [
    # Client urls
    path('clients/', ClientListCreateAPIView.as_view(), name='patient_list_create'),
    path('clients/<int:pk>', ClientRetrieveUpdateDestroyAPIView.as_view(), name='patient-detail'),

    # Turn urls
    path('turns/', TurnListCreateAPIView.as_view(), name='turn-list-create'),
    path('turns/<int:pk>', TurnRetrieveUpdateDestroyAPIView.as_view(), name='turn-detail-update-delete'),
    path('turns/full-detail/', TurnFullDetailAPIView.as_view(), name='turn-full-detail-list'),
    path('turns/full-detail/<int:pk>', TurnFullDetailRetrieveAPIView.as_view(), name='turn-full-detail'),
    path('turns/doctor/<int:pk>', DoctorTurnUpdateAPIView.as_view(), name='doctor-turn-update'),
    path('turns/doctor/', DoctorTurnListAPIView.as_view(), name='doctor-turn-list'),
    path('turns/cancel/<int:pk>', TurnCancelAPIView.as_view(), name='turn-cancel'),

    # Pateint urls
    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyAPIView.as_view(), name='patient-detail'),

    # PatientService URLs
    path('patient-services/', PatientServiceListCreateAPIView.as_view(), name='patient-service-list-create'),
    path('patient-services/<int:pk>/', PatientServiceRetrieveUpdateDestroyAPIView.as_view(),
         name='patient-service-detail'),

    # PatientService URLs
    path('patient-payment/', PatientPaymentListCreateAPIView.as_view(), name='patient-payment-list-create'),
    path('patient-payment/<int:pk>/', PatientPaymentRetrieveUpdateDestroyAPIView.as_view(),
         name='patient-payment-detail'),

    # Report
    path('report/', ReportView.as_view(), name='report')

]
