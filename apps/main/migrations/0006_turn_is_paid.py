# Generated by Django 5.1.4 on 2025-01-09 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_patient_total_remainder'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='is_paid',
            field=models.BooleanField(default=True),
        ),
    ]
