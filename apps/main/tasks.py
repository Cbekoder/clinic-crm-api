from celery import shared_task
from apps.main.models import Patient
from django.utils.timezone import now

@shared_task
def update_patient_sums():
    current_time = now()
    patients = Patient.objects.filter(is_finished=False)

    for patient in patients:
        if patient.room and patient.room.seat_price:
            patient.total_sum += patient.room.seat_price
            patient.total_remainder += patient.room.seat_price
            patient.save()

    return f"Successfully updated {patients.count()} patients."


if __name__ == "__main__":
    update_patient_sums()