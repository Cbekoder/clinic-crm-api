from rest_framework import serializers
from rest_framework.serializers import DateTimeField
from apps.stuff.serializers import ServiceSerializer, SectionSerializer, RoomSerializer
from apps.users.serializers import UserSimpleDetailSerializer
from .models import Client, Turn, Patient, PatientService, PatientPayment


class ClientSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Client
        fields = '__all__'


class TurnGetSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    client = ClientSerializer()
    doctor = UserSimpleDetailSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Turn
        fields = ['id', "client", "doctor", "service", "price", "turn_num", "status", "created_at"]
        read_only_fields = ["turn_num", "created_at"]

class TurnFullDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    client = ClientSerializer()
    doctor = UserSimpleDetailSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Turn
        fields = ['id', "client", "doctor", "service", "price", "turn_num", "status", 'complaint', 'diagnosis', 'analysis_result', 'prescription', "created_at"]
        read_only_fields = ["turn_num", "created_at"]

class TurnPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Turn
        fields = [
            'id', 'client', 'service', 'doctor', 'price', 'turn_num',
            'appointment_time', 'is_paid', 'created_at'
        ]
        read_only_fields = ["turn_num", "created_at"]

    def to_representation(self, instance):
        # representation = super().to_representation(instance)
        return TurnGetSerializer(instance).data

class TurnUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = ['id', 'complaint', 'diagnosis', 'analysis_result', 'prescription']


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
    register_date = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    finished_date = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Patient
        fields = [
            'id', 'client', 'section', 'room', 'doctor', 'register_date',
            'is_finished', 'finished_date', 'total_sum', 'total_remainder'
        ]

class PatientPostSerializer(serializers.ModelSerializer):
    register_date = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    finished_date = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Patient
        fields = [
            'id', 'client', 'section', 'room', 'doctor', 'register_date',
            'is_finished', 'finished_date', 'total_sum', 'total_remainder'
        ]
        read_only_fields = ["register_date", "finished_date", "total_sum", "total_remainder"]

    def to_representation(self, instance):
        # representation = super().to_representation(instance)
        return PatientSerializer(instance).data


class PatientServiceSerializer(serializers.ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = PatientService
        fields = ['id', 'patient', 'service', 'price', 'created_at']
        read_only_fields = ["created_at"]

class PatientServiceDetailSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    service = ServiceSerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = PatientService
        fields = ['id', 'patient', 'service', 'price', 'created_at']
        read_only_fields = ["created_at"]


class PatientPaymentSerializer(serializers.ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = PatientPayment
        fields = ['id', 'patient', 'summa', 'description', 'created_at']
        read_only_fields = ["created_at"]

class PatientPaymentDetailSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = PatientPayment
        fields = ['id', 'patient', 'summa', 'description', 'created_at']
        read_only_fields = ["created_at"]


class PatientDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    section = SectionSerializer()
    room = RoomSerializer()
    doctor = UserSimpleDetailSerializer()
    services = PatientServiceDetailSerializer(source='patientservice_set', many=True, read_only=True)
    payments = PatientPaymentDetailSerializer(source='patientpayment_set', many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'client', 'section', 'room', 'doctor', 'register_date',
            'is_finished', 'finished_date', 'total_sum', 'total_remainder', 'services', 'payments'
        ]