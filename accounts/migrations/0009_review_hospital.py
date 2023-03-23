# Generated by Django 3.2 on 2023-03-22 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20230323_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_reviews', to='accounts.hospital', verbose_name='Doctor'),
        ),
    ]