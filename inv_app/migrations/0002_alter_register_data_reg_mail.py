# Generated by Django 5.0.4 on 2024-10-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_data',
            name='reg_mail',
            field=models.EmailField(max_length=40),
        ),
    ]
