from rest_framework import serializers
from .models import Section, Room, Service

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']

class RoomSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'section', 'section_name', 'number', 'all_seats', 'free_seats', 'seat_price']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'room']
