# Generated by Django 5.1.4 on 2025-01-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='role',
            field=models.CharField(choices=[('shifokor', 'Shifokor'), ('hamshira', 'Hamshira'), ('boshqa', 'Boshqa hodim'), ('admin', 'Admin'), ('ceo', 'CEO')], max_length=30),
        ),
    ]
