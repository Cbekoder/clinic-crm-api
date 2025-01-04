# Generated by Django 5.1.4 on 2025-01-04 14:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stuff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('extra_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Mijoz ',
                'verbose_name_plural': 'Mijozlar ',
            },
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('turn_num', models.PositiveIntegerField()),
                ('turn_type', models.CharField(choices=[('0', 'Doctor'), ('1', 'Service')], default='0', max_length=10)),
                ('status', models.CharField(choices=[('new', 'New'), ('active', 'Active'), ('pending', 'Pending'), ('closed', 'Closed'), ('canceled', 'Canceled')], default='new', max_length=25)),
                ('appointment_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.TextField(blank=True, help_text='Shikoyat', null=True)),
                ('diagnosis', models.TextField(blank=True, help_text='Tashxis', null=True)),
                ('analysis_result', models.TextField(blank=True, help_text='Analiz javoblari', null=True)),
                ('prescription', models.TextField(blank=True, help_text='Dori-darmon retsepti', null=True)),
                ('is_canceled', models.BooleanField(default=False)),
                ('cancel_reason', models.TextField(blank=True, null=True)),
                ('cancel_refund', models.FloatField(blank=True, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.patient')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stuff.service')),
            ],
            options={
                'verbose_name': 'Navbat',
                'verbose_name_plural': 'Navbatlar',
                'ordering': ['-created_at'],
            },
        ),
    ]
