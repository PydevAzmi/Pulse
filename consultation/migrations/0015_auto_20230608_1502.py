# Generated by Django 3.2 on 2023-06-08 12:02

import consultation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0014_auto_20230526_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='ct',
            field=models.ImageField(blank=True, null=True, upload_to=consultation.models.patient_dir_path, verbose_name='CT'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='mri',
            field=models.ImageField(blank=True, null=True, upload_to=consultation.models.patient_dir_path, verbose_name='MRI'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Title'),
        ),
    ]
