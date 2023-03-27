# Generated by Django 3.2 on 2023-03-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0006_auto_20230325_0117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitalconsultationrequest',
            old_name='accepted_doctor',
            new_name='accepted_hospitals',
        ),
        migrations.AddField(
            model_name='survey',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True, verbose_name='Gender'),
        ),
    ]