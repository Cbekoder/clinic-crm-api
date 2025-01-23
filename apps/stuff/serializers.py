from rest_framework.serializers import ModelSerializer, DateTimeField, CharField
from .models import Section, Room, Service, Expense


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name']

class RoomSerializer(ModelSerializer):
    section_name = CharField(source='section.name', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'section', 'section_name', 'number', 'all_seats', 'free_seats', 'seat_price', 'for_patient']

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'room']
        

class ExpenseListSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'reason', 'description', 'total_sum', 'created_at']
        read_only_fields = ['id', 'created_at']

class ExpenseRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'reason', 'description', 'total_sum', 'created_at']
        read_only_fields = ['id', 'created_at', 'total_sum']
