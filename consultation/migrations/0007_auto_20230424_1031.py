# Generated by Django 3.2 on 2023-04-24 08:31

import consultation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0006_mlmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='ct',
            field=models.ImageField(upload_to=consultation.models.patient_dir_path, verbose_name='CT'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='ecg',
            field=models.ImageField(upload_to=consultation.models.patient_dir_path, verbose_name='ECG'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='mri',
            field=models.ImageField(upload_to=consultation.models.patient_dir_path, verbose_name='MRI'),
        ),
    ]
