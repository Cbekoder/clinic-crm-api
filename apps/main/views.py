from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from django.utils.dateparse import parse_date


from .models import Patient, Turn
from .serializers import PatientSerializer, TurnGetSerializer, TurnPostSerializer, TurnCancelSerializer


class PatientListCreateAPIView(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer



class TurnListCreateAPIView(ListCreateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnGetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['doctor__first_name', 'doctor__last_name',
                     'doctor__room', 'service__name', 'service__room',
                     'patient__first_name', 'patient__last_name', 'turn_num']

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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurnGetSerializer
        return TurnPostSerializer

class TurnCancelAPIView(UpdateAPIView):
    queryset = Turn.objects.all()
    serializer_class = TurnCancelSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        turn = self.get_object()
        if turn.is_canceled:
            raise ValidationError("This turn is already canceled.")
        serializer.save()




