from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from .models import Position, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.position:
            data['role'] = self.user.position.role
        else:
            ValidationError({"error": "User position shouldn't be None"})
        return data


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'middle_name', 'email',
            'birth_date', 'phone_number', 'extra_phone_number', 'balance',
            'status', 'employment_date', 'working_time', 'is_active', 'date_joined'
        ]
        read_only_fields = ['balance', 'date_joined', 'is_active']


class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password will be write-only

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'middle_name',
            'birth_date', 'phone_number', 'extra_phone_number',
            'room', 'position', 'status', 'employment_date', 'working_time'
        ]

    def validate_position(self, value):
        if value.role != '1':  # Ensure position is 'Shifokor'
            raise serializers.ValidationError("Position must be 'Shifokor'")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user


class NurseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password will be write-only

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'middle_name',
            'birth_date', 'phone_number', 'extra_phone_number',
            'room', 'position', 'status', 'employment_date', 'working_time'
        ]

    def validate_position(self, value):
        if value.role != '2':  # Ensure position is 'Hamshira'
            raise serializers.ValidationError("Position must be 'Hamshira'")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

class OtherStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # password will be write-only

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'middle_name',
            'birth_date', 'phone_number', 'extra_phone_number',
            'room', 'position', 'status', 'employment_date', 'working_time'
        ]

    def validate_position(self, value):
        if value.role != '3':  # Ensure position is 'Hamshira'
            raise serializers.ValidationError("Position must be 'Boshqa'")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
