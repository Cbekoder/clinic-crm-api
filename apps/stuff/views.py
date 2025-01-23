from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.users.permissions import IsCEO, IsAdmin, IsDoctor, IsRegistrator
from .models import Section, Room, Service, Expense
from .serializers import SectionSerializer, RoomSerializer, ServiceSerializer, ExpenseListSerializer, \
    ExpenseRetrieveSerializer


class SectionListCreateAPIView(ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin]
        return [permission() for permission in permission_classes]

class SectionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin]
        return [permission() for permission in permission_classes]

class RoomListCreateAPIView(ListCreateAPIView):
    serializer_class = RoomSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="for_doctors",
                in_=openapi.IN_QUERY,
                description="Filter rooms by patient availability. Use `true` for patient rooms and `false` for others.",
                type=openapi.TYPE_BOOLEAN,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Room.objects.all()
        for_doctors = self.request.query_params.get('for_doctors', None)
        if for_doctors is not None and for_doctors == "true":
            queryset = queryset.filter(for_patient=False)
        else:
            queryset = queryset.filter(for_patient=True)
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin]
        return [permission() for permission in permission_classes]

class RoomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin]
        return [permission() for permission in permission_classes]

class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin]
        return [permission() for permission in permission_classes]


class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        else:
            permission_classes = [IsCEO | IsAdmin]
        return [permission() for permission in permission_classes]


class ExpensesListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'reason', 'description']
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            if not parse_date(start_date):
                raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
            self.queryset = self.queryset.filter(created_at__date__gte=start_date)

        if end_date:
            if not parse_date(end_date):
                raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
            self.queryset = self.queryset.filter(created_at__date__lte=end_date)

        return self.queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense colums: id, reason, description.",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ExpenseListSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseRetrieveSerializer
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]