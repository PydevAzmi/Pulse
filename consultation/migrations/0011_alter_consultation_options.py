# Generated by Django 3.2 on 2023-04-26 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0010_alter_consultation_survey'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultation',
            options={'verbose_name': 'Consultation Requests', 'verbose_name_plural': 'Consultations'},
        ),
    ]
