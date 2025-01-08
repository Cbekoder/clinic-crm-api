from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from django.db.models import Q
from django.utils.dateparse import parse_date
from apps.users.permissions import IsCEO, IsAdmin, IsDoctor, IsRegistrator


from .models import Client, Turn, Patient, PatientService, PatientPayment
from .serializers import ClientSerializer, TurnGetSerializer, TurnPostSerializer, TurnCancelSerializer, \
    PatientSerializer, PatientServiceSerializer, TurnUpdateSerializer, PatientPostSerializer, PatientDetailSerializer, \
    PatientPaymentSerializer


class ClientListCreateAPIView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin | IsRegistrator]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search clients by first name, last name, middle name, phone number, or address",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(middle_name__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(extra_phone_number__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        return queryset


class ClientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin | IsRegistrator]
        return [permission() for permission in permission_classes]


class TurnListCreateAPIView(ListCreateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnGetSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
    filter_backends = [SearchFilter]
    search_fields = ['doctor__first_name', 'doctor__last_name',
                     'doctor__room', 'service__name', 'service__room',
                     'client__first_name', 'client__last_name', 'turn_num']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurnGetSerializer
        return TurnPostSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Filter turns created on or after this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format="date"
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Filter turns created on or before this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format="date"
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by doctor(first_name, last_name, room), service(name, room), client(first_name, last_name), turn_num.",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', str(date.today()))
        end_date = self.request.query_params.get('end_date', str(date.today()))

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        self.queryset =self.queryset.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        return self.queryset

class TurnRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnGetSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurnGetSerializer
        return TurnPostSerializer

class DoctorTurnUpdateAPIView(UpdateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnUpdateSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        user = self.request.user
        if user.role  == 'doctor':
            return self.queryset.filter(doctor=user)
        return self.queryset.none()

    def perform_update(self, serializer):
        turn = serializer.instance
        if turn.doctor != self.request.user:
            raise ValidationError({"detail": "You can only update your assigned turns."})
        serializer.save()

class TurnCancelAPIView(UpdateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnCancelSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def perform_update(self, serializer):
        turn = self.get_object()
        if turn.is_canceled:
            raise ValidationError("This turn is already canceled.")
        serializer.save()


class PatientListCreateAPIView(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientSerializer
        return PatientPostSerializer

class PatientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientDetailSerializer
        return PatientPostSerializer

class PatientServiceListCreateAPIView(ListCreateAPIView):
    queryset = PatientService.objects.all()
    serializer_class = PatientServiceSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]


class PatientServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PatientService.objects.all()
    serializer_class = PatientServiceSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]


class PatientPaymentListCreateAPIView(ListCreateAPIView):
    queryset = PatientPayment.objects.all()
    serializer_class = PatientPaymentSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]


class PatientPaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PatientPayment.objects.all()
    serializer_class = PatientPaymentSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]




