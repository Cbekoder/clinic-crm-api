from django.db.models.sql.constants import SINGLE
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from .models import Position, User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, DoctorSerializer, \
    SinglePositionSerializer, NurseSerializer, OtherStaffSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Position Views
class PositionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = SinglePositionSerializer

class DoctorPositions(ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = SinglePositionSerializer

    def get_queryset(self):
        return self.queryset.filter(role='1')

    def perform_create(self, serializer):
        serializer.save(role='1')

class NursePositions(ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = SinglePositionSerializer

    def get_queryset(self):
        return self.queryset.filter(role='2')

    def perform_create(self, serializer):
        serializer.save(role='2')

class OtherPositions(ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = SinglePositionSerializer

    def get_queryset(self):
        return self.queryset.filter(role='3')

    def perform_create(self, serializer):
        serializer.save(role='3')



# User Views
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DoctorCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return self.queryset.filter(position__role='1')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DoctorSerializer
        return UserSerializer

    def perform_create(self, serializer):
        # Fetch the position from the POST request
        position = self.request.data.get('position')
        if position:
            position_obj = Position.objects.get(id=position)
            if position_obj.role != '1':  # Check if it's 'Shifokor'
                raise ValidationError("Position must be 'Shifokor'")

        serializer.save()

class NurseCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = NurseSerializer

    def get_queryset(self):
        return self.queryset.filter(position__role='2')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NurseSerializer
        return UserSerializer

    def perform_create(self, serializer):
        # Fetch the position from the POST request
        position = self.request.data.get('position')
        if position:
            position_obj = Position.objects.get(id=position)
            if position_obj.role != '2':  # Check if it's 'Hamshira'
                raise ValidationError("Position must be 'Hamshira'")

        serializer.save()


class OtherStaffCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = OtherStaffSerializer

    def get_queryset(self):
        return self.queryset.filter(position__role='3')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OtherStaffSerializer
        return UserSerializer

    def perform_create(self, serializer):
        # Fetch the position from the POST request
        position = self.request.data.get('position')
        if position:
            position_obj = Position.objects.get(id=position)
            if position_obj.role != '3':  # Check if it's 'Boshqa'
                raise ValidationError("Position must be 'Boshqa'")

        serializer.save()