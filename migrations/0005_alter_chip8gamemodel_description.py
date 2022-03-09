# Generated by Django 4.0.2 on 2022-03-08 05:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chip8', '0004_alter_chip8gamemodel_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chip8gamemodel',
            name='description',
            field=models.TextField(max_length=2000, null=True, validators=[django.core.validators.MaxLengthValidator(2000)]),
        ),
    ]