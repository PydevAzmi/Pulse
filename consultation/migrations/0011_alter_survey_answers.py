# Generated by Django 3.2 on 2023-03-26 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0010_alter_question_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='answers',
            field=models.ManyToManyField(related_name='survey_answers', to='consultation.Answer', verbose_name='Answers'),
        ),
    ]