# Generated by Django 5.1.4 on 2025-01-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_client_options_alter_patient_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='total_remainder',
            field=models.FloatField(default=0),
        ),
    ]
