from django.contrib import admin
from .models import Client, Turn, Patient, PatientService

class PatientServiceInline(admin.StackedInline):
    model = PatientService
    extra = 1  # Number of extra empty forms in the inline
    # readonly_fields = ['price']  # Make price field read-only in the inline

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')

@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ('client', 'doctor', 'service', 'turn_num', 'status', 'appointment_time')
    list_filter = ('turn_type', 'status', 'appointment_time')
    search_fields = ('client__first_name', 'client__last_name', 'doctor__first_name', 'doctor__last_name')
    ordering = ('-appointment_time',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('client', 'doctor', 'section', 'room', 'register_date', 'is_finished', 'total_sum')
    list_filter = ('is_finished', 'register_date')
    search_fields = ('client__first_name', 'client__last_name', 'doctor__first_name', 'doctor__last_name')
    inlines = [PatientServiceInline]  # Add the inline here
