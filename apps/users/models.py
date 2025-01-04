from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import BaseModel

ROLE_CHOICES = (
    ('shifokor', 'Shifokor'),
    ('hamshira', 'Hamshira'),
    ('boshqa', 'Boshqa hodim'),
    ('admin', 'Admin'),
    ('ceo', 'CEO')
)

STATUS_CHOICES = (
    ("active", "Faol"),
    ("inactive", "Nofaol")
)


class Position(BaseModel):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = "Lavozim "
        verbose_name_plural = "Lavozimlar"

    def __str__(self):
        return self.name

class User(AbstractUser, BaseModel):
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    extra_phone_number = models.CharField(max_length=15, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    kpi = models.FloatField(null=True, blank=True)
    balance = models.FloatField(default=0)
    room = models.CharField(max_length=100, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="active")
    employment_date = models.DateField(null=True, blank=True)
    working_time = models.TextField(null=True, blank=True, help_text="Ish vaqti va kunlari, Namuna: Du-Ju 9:00-17:00")


    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar"
