from celery import shared_task
from .models import User
from datetime import date

@shared_task
def add_salaries_to_balance():
    today = date.today()
    if today.day == 1:  # Ensure this only runs on the 1st of the month
        users = User.objects.exclude(salary__isnull=True)  # Exclude users with no salary
        for user in users:
            user.balance += user.salary
            user.save()
    return f"{users.count()} users updated."
