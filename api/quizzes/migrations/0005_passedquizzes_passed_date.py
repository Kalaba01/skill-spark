# Generated by Django 5.1.5 on 2025-02-18 20:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_passedquizzes'),
    ]

    operations = [
        migrations.AddField(
            model_name='passedquizzes',
            name='passed_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
