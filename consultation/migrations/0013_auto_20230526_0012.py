# Generated by Django 3.2 on 2023-05-25 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
        ('consultation', '0012_alter_consultation_doctors'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='hospital',
            field=models.ManyToManyField(related_name='consultations_hospital', to='accounts.Hospital'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='doctors',
            field=models.ManyToManyField(related_name='consultations_doctor', to='accounts.Doctor'),
        ),
    ]
