# Generated by Django 5.0.6 on 2024-06-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('user', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('tema', models.CharField(max_length=25)),
            ],
        ),
    ]
