# Generated by Django 3.2 on 2023-04-25 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
        ('consultation', '0007_auto_20230424_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_report', to='accounts.doctor'),
        ),
        migrations.AlterField(
            model_name='review',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.patient'),
        ),
    ]
