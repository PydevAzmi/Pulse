# Generated by Django 3.2 on 2023-03-21 20:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230321_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_hospital',
            field=models.BooleanField(default=False, verbose_name='Is Hospital'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(validators=[django.core.validators.MaxLengthValidator(5), django.core.validators.MinLengthValidator(0)], verbose_name='Rate')),
                ('review', models.TextField(max_length=500, verbose_name='Review')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('Doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.doctor', verbose_name='Doctor')),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient', verbose_name='Patient')),
            ],
        ),
    ]
