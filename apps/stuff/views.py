from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.users.permissions import IsCEO, IsAdmin, IsDoctor, IsRegistrator
from .models import Section, Room, Service
from .serializers import SectionSerializer, RoomSerializer, ServiceSerializer


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
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # permission_classes = [IsCEO | IsAdmin | IsDoctor | IsRegistrator]

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
