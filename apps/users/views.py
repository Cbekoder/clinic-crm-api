from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from .models import Position, User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, DoctorSerializer, \
    PositionSerializer, NurseSerializer, OtherStaffSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfile(APIView):
    def get(self):
        if self.request.user.is_authenticated:
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data)
            

# Position Views
class PositionsListCreateAPIView(ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def get_queryset(self):
        queryset = Position.objects.all()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class PositionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer



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