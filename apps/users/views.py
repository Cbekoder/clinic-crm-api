from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import IsCEO, IsAdmin, IsDoctor, IsRegistrator
from .models import User, SalaryPayment
from .filters import UserFilter
from .serializers import UserDetailSerializer, UserPostSerializer, CustomTokenObtainPairSerializer, \
    PasswordUpdateSerializer, SalaryPaymentPostSerializer, SalaryPaymentGetSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# User Views
class UserProfile(APIView):
    def get(self, request):
        if self.request.user.is_authenticated:
            serializer = UserDetailSerializer(self.request.user)
            return Response(serializer.data)

class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsCEO | IsAdmin]
        else:
            permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]
        return [permission() for permission in permission_classes]

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer


class PasswordUpdateView(APIView):
    permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

    @swagger_auto_schema(
        operation_description="Update the authenticated user's password.",
        request_body=PasswordUpdateSerializer,
    )
    def put(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsCEO | IsAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['staff__first_name', 'staff__last_name', 'staff__username']
    filterset_fields = ['staff']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalaryPaymentGetSerializer
        return SalaryPaymentPostSerializer

class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentPostSerializer
    permission_classes = [IsCEO | IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalaryPaymentGetSerializer
        return SalaryPaymentPostSerializer