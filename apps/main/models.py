from django.db import models, transaction
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from datetime import date

from apps.common.models import BaseModel
from apps.stuff.models import Service, Section, Room
from apps.users.models import User


class Client(BaseModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    extra_phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Mijoz "
        verbose_name_plural = "Mijozlar "

    @property
    def full_name(self):
        return self.first_name + self.last_name

    def __str__(self):
        return self.full_name



TURN_CHOICE = (
    ('0', 'Doctor'),
    ('1', 'Service')
)

STATUS_CHOICES = (
    ('new', 'New'),
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('closed', 'Closed'),
    ('canceled', 'Canceled')
)

class Turn(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    turn_num = models.PositiveIntegerField()
    turn_type = models.CharField(max_length=10, choices=TURN_CHOICE, default='0')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="new")
    appointment_time = models.DateTimeField(default=now)
    # for doctor
    complaint = models.TextField(null=True, blank=True, help_text="Shikoyat") # Shikoyat
    diagnosis = models.TextField(null=True, blank=True, help_text="Tashxis") # Tashxis
    analysis_result = models.TextField(null=True, blank=True, help_text="Analiz javoblari") # Analiz javoblari
    prescription = models.TextField(null=True, blank=True, help_text="Dori-darmon retsepti") # Dori-darmon retsepti
    # for cancel
    is_canceled = models.BooleanField(default=False)
    cancel_reason = models.TextField(null=True, blank=True)
    cancel_refund = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Navbat"
        verbose_name_plural = "Navbatlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.client.last_name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            today = date.today()
            if self.doctor:
                room = self.doctor.room
                last_turn = Turn.objects.filter(
                    doctor__room=room,
                    turn_type='0',
                    created_at__date=today
                ).order_by('-turn_num').first()
                self.turn_type = "0"
            elif self.service:
                room = self.service.room
                last_turn = Turn.objects.filter(
                    service__room=room,
                    turn_type='1',
                    created_at__date=today
                ).order_by('-turn_num').first()
                self.turn_type = "1"
            else:
                raise ValidationError({"error": "Service or Doctor is required."})

            self.turn_num = last_turn.turn_num + 1 if last_turn else 1

            super().save(*args, **kwargs)


class Patient(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    register_date = models.DateTimeField(default=now)
    is_finished = models.BooleanField(default=False)
    finished_date = models.DateTimeField(null=True)
    total_sum = models.FloatField(default=0)

    class Meta:
        verbose_name = "Bemor "
        verbose_name_plural = "Bemorlar"

    def __str__(self):
        return self.client.full_name


class PatientService(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Bemor xizmat "
        verbose_name_plural = "Bemor xizmatlari "

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.patient.total_sum += self.service.price

            super().save(*args, **kwargs)





