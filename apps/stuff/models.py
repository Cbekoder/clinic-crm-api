from django.db import models
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator
from apps.common.models import BaseModel


class Section(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Bo'lim "
        verbose_name_plural = "Bo'limlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Room(BaseModel):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    number =models.CharField(max_length=20)
    all_seats = models.IntegerField(default=1)
    free_seats = models.IntegerField()
    seat_price = models.FloatField(validators=[MinValueValidator(0.0)])
    for_patient = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Xona "
        verbose_name_plural = "Xonalar "
        ordering = ['-created_at']

    def clean(self):
        if self.free_seats > self.all_seats:
            raise ValidationError("Free seats cannot exceed all seats.")

    def __str__(self):
        return f"{self.number}"


class Service(BaseModel):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    room = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ['-id']

    def __str__(self):
        return self.name

class Expense(models.Model):
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = 'Xarajat '
        verbose_name_plural = 'Xarajatlar '
        ordering = ['-created_at']