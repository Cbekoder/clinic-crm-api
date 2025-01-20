from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, ListAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from django.db.models import Q, Sum
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsCEO, IsAdmin, IsDoctor, IsRegistrator


from .models import Client, Turn, Patient, PatientService, PatientPayment
from .serializers import ClientSerializer, TurnGetSerializer, TurnPostSerializer, TurnCancelSerializer, \
    PatientSerializer, PatientServiceSerializer, TurnUpdateSerializer, PatientPostSerializer, PatientDetailSerializer, \
    PatientPaymentSerializer, TurnFullDetailSerializer, CanceledTurnSerializer
from ..stuff.models import Service
from ..stuff.serializers import ServiceSerializer
from ..users.models import User
from ..users.serializers import UserSimpleDetailSerializer


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
    permission_classes = [IsDoctor, IsAuthenticated]
    queryset = Turn.objects.all()
    serializer_class = TurnUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role  == 'doctor':
            return self.queryset.filter(doctor=user)
        return self.queryset.none()

    def perform_update(self, serializer):
        turn = serializer.instance
        if turn.doctor != self.request.user:
            raise ValidationError({"detail": "You can only update your assigned turns."})
        serializer.save(status="closed")

class DoctorTurnListAPIView(ListAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnFullDetailSerializer
    permission_classes = [IsDoctor, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role  == 'doctor':
            return self.queryset.filter(doctor=user)
        return self.queryset.none()

class TurnCancelAPIView(UpdateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnCancelSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def perform_update(self, serializer):
        turn = self.get_object()
        if turn.is_canceled:
            raise ValidationError("This turn is already canceled.")
        serializer.save()

class TurnCanceledListAPIView(ListAPIView):
    queryset = Turn.objects.all()
    serializer_class = CanceledTurnSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def get_queryset(self):
        return self.queryset.filter(is_canceled=True)

class TurnCanceledRetrieveAPIView(RetrieveAPIView):
    queryset = Turn.objects.all()
    serializer_class = CanceledTurnSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def get_queryset(self):
        return self.queryset.filter(is_canceled=True)

class TurnFullDetailAPIView(ListAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnFullDetailSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]


class TurnFullDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnFullDetailSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]


class PatientListCreateAPIView(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date for the report (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format="date"),
            openapi.Parameter(
                'is_finished',
                openapi.IN_QUERY,
                description="Filter patients by their finished status (true or false)",
                type=openapi.TYPE_BOOLEAN
            )]

    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PatientSerializer
        return PatientPostSerializer

    def get_queryset(self):
        is_finished = self.request.query_params.get('is_finished')

        if is_finished is not None:
            self.queryset.filter(is_finished=is_finished.lower() in ['true', '1', 't'])
        else:
            self.queryset.filter(is_finished=False)

        return self.queryset


class DoctorPatientListAPIView(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsDoctor, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role  == 'doctor':
            return self.queryset.filter(doctor=user)
        return self.queryset.none()

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



class ReportView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date for the report (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format="date"),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date for the report (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, format="date"),
            openapi.Parameter('doctor', openapi.IN_QUERY, description="Doctor ID to filter by",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('service', openapi.IN_QUERY, description="Service ID to filter by",
                              type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', str(date.today()))
        end_date = request.query_params.get('end_date', str(date.today()))

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        if not start_date or not end_date:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        turns = Turn.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        doctor_id = request.query_params.get('doctor')
        service_id = request.query_params.get('service')

        if doctor_id:
            turns = turns.filter(doctor_id=doctor_id)

        if service_id:
            turns = turns.filter(service_id=service_id)

        total_sum = turns.aggregate(total_price=Sum('price'))['total_price']
        total_paid = turns.filter(is_paid=True).aggregate(total_price=Sum('price'))['total_price']

        doctors = User.objects.filter(role="doctor")
        services = Service.objects.all()

        doctor_total = 0
        doctor_report = []
        for doctor in doctors:
            total_price = turns.filter(doctor=doctor, turn_type=0).aggregate(total_price=Sum('price'))[
                              'total_price'] or 0
            doctor_data = UserSimpleDetailSerializer(doctor).data
            if total_price > 0:
                doctor_total += total_price
                doctor_report.append({
                    "doctor": doctor_data,
                    "total_price": total_price
                })

        service_total = 0
        service_report = []
        for service in services:
            total_price = turns.filter(service=service, turn_type=1).aggregate(total_price=Sum('price'))[
                              'total_price'] or 0
            service_data = ServiceSerializer(service).data
            if total_price > 0:
                service_total += total_price
                service_report.append({
                    "service": service_data,
                    "total_price": total_price
                })

        # Client payments aggregation
        clients = Client.objects.all()
        client_report = []
        clients_total = 0

        for client in clients:
            total_price = PatientPayment.objects.filter(
                patient__client=client,
                created_at__date__gte=start_date,
                created_at__date__lte=end_date
            ).aggregate(total_summa=Sum('summa'))['total_summa'] or 0

            if total_price > 0:
                clients_total += total_price
                client_data = {
                    "id": client.id,
                    "full_name": client.full_name,
                }
                client_report.append({
                    "client": client_data,
                    "total_price": total_price
                })

        return Response({
            "total_price": total_sum,
            "total_paid": total_paid,
            "start_date": start_date,
            "end_date": end_date,
            "doctors_total": doctor_total,
            "doctor_report": doctor_report,
            "services_total": service_total,
            "service_report": service_report,
            "clients_total": clients_total,
            "client_report": client_report
        })


