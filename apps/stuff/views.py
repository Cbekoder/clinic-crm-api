from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Section, Room, Service
from .serializers import SectionSerializer, RoomSerializer, ServiceSerializer


class SectionListCreateAPIView(ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SectionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class RoomListCreateAPIView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# Retrieve, Update, and Delete view
class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
