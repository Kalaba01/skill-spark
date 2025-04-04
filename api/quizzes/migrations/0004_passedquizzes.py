# Generated by Django 5.1.5 on 2025-02-16 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('quizzes', '0003_remove_quiz_document_remove_quiz_document_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassedQuizzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passed_quizzes', to='authentication.employee')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passed_by_employees', to='quizzes.quiz')),
            ],
            options={
                'unique_together': {('employee', 'quiz')},
            },
        ),
    ]
