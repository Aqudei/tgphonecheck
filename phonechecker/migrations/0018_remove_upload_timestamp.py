# Generated by Django 3.2.8 on 2021-10-15 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phonechecker', '0017_check_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='timestamp',
        ),
    ]
