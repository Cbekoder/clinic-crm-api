from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import BaseModel

ROLE_CHOICES = (
    ('ceo', 'CEO'),
    ('admin', 'Admin'),
    ('doctor', 'Shifokor'),
    ('registrator', 'Registrator'),
    ('other', 'Boshqa hodim')
)

STATUS_CHOICES = (
    ("active", "Faol"),
    ("inactive", "Nofaol")
)

GENDER_CHOICES = (
    ("male", "Erkak"),
    ("female", "Ayol")
)


class User(AbstractUser, BaseModel):
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    extra_phone_number = models.CharField(max_length=15, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    kpi = models.FloatField(null=True, blank=True)
    balance = models.FloatField(default=0)
    room = models.CharField(max_length=100, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, help_text="Role bo'lishi mumkin: 'ceo', 'admin', 'doctor', 'registrator' 'other'", default="other")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, help_text="Status bo'lishi mumkin: 'active', 'inactive'", default="active")
    employment_date = models.DateField(null=True, blank=True)
    working_time = models.TextField(null=True, blank=True, help_text="Ish vaqti va kunlari, Namuna: Du-Ju 9:00-17:00")


    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.username
