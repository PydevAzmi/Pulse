# Generated by Django 3.2 on 2023-03-25 21:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0007_auto_20230325_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorconsultationrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejeted')], default='pending', max_length=50, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='hospitalconsultationrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejeted')], default='pending', max_length=50, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Age'),
        ),
    ]