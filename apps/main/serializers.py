from rest_framework import serializers
from .models import Patient, Turn
from apps.stuff.serializers import ServiceSerializer
from apps.users.serializers import DoctorSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class TurnGetSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    patient = PatientSerializer
    doctor = DoctorSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Turn
        fields = ["patient", "doctor", "service", "price", "turn_num", "status", "created_at"]
        read_only_fields = ["turn_num", "created_at"]

class TurnPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Turn
        fields = [
            'id', 'patient', 'service', 'doctor', 'price', 'turn_num',
            'appointment_time', 'created_at'
        ]
        read_only_fields = ["turn_num", "created_at"]

    def to_representation(self, instance):
        # representation = super().to_representation(instance)
        return TurnGetSerializer(instance).data


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

