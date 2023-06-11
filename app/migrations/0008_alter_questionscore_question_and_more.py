# Generated by Django 4.1.3 on 2023-06-06 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_answerscore_questionscore_delete_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionscore',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionscores', to='app.question'),
        ),
        migrations.AlterField(
            model_name='questionscore',
            name='value',
            field=models.SmallIntegerField(choices=[(1, 'Positive'), (-1, 'Negative')], verbose_name='Value'),
        ),
    ]