# Generated by Django 4.0.4 on 2022-05-07 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='year_of_publish',
            field=models.DateField(),
        ),
    ]
