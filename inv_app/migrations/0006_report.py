# Generated by Django 5.0.4 on 2024-10-20 16:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv_app', '0005_tasklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=20)),
                ('task_date', models.DateField()),
                ('closed_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
