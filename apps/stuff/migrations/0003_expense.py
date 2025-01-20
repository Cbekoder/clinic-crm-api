# Generated by Django 5.1.4 on 2025-01-19 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0002_alter_room_options_alter_section_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('total_sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Xarajat ',
                'verbose_name_plural': 'Xarajatlar ',
                'ordering': ['-created_at'],
            },
        ),
    ]
