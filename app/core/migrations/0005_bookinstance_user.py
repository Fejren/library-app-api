# Generated by Django 4.0.4 on 2022-05-10 15:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_num_of_pages_book_number_of_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
