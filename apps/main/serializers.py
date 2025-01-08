from rest_framework import serializers
from .models import Client, Turn, Patient, PatientService
from apps.stuff.serializers import ServiceSerializer, SectionSerializer, RoomSerializer
from ..users.serializers import UserSimpleDetailSerializer


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class TurnGetSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    client = ClientSerializer
    doctor = UserSimpleDetailSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Turn
        fields = ["client", "doctor", "service", "price", "turn_num", "status", "created_at"]
        read_only_fields = ["turn_num", "created_at"]

class TurnPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Turn
        fields = [
            'id', 'client', 'service', 'doctor', 'price', 'turn_num',
            'appointment_time', 'created_at'
        ]
        read_only_fields = ["turn_num", "created_at"]

    def to_representation(self, instance):
        # representation = super().to_representation(instance)
        return TurnGetSerializer(instance).data

class TurnUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = ['complaint', 'diagnosis', 'analysis_result', 'prescription']
        extra_kwargs = {
            'complaint': {'required': True},
            'diagnosis': {'required': True},
            'analysis_result': {'required': True},
            'prescription': {'required': True},
        }


class TurnCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = ['cancel_reason', 'cancel_refund']

    def update(self, instance, validated_data):
        if not instance.is_canceled:
            instance.is_canceled = True
            instance.cancel_reason = validated_data.get('cancel_reason', instance.cancel_reason)
            instance.cancel_refund = validated_data.get('cancel_refund', instance.cancel_refund)
            instance.save()
        else:
            raise serializers.ValidationError("This turn is already canceled.")
        return instance


class PatientSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    section = SectionSerializer()
    room = RoomSerializer()
    doctor = UserSimpleDetailSerializer()
    class Meta:
        model = Patient
        fields = [
            'id', 'client', 'section', 'room', 'doctor', 'register_date',
            'is_finished', 'finished_date', 'total_sum'
        ]

class PatientPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'client', 'section', 'room', 'doctor', 'register_date',
            'is_finished', 'finished_date', 'total_sum'
        ]

    def to_representation(self, instance):
        # representation = super().to_representation(instance)
        return PatientSerializer(instance).data


class PatientServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientService
        fields = ['id', 'patient', 'service', 'price']
