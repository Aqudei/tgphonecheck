# Generated by Django 3.2.8 on 2021-10-08 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonechecker', '0003_auto_20211007_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=None, verbose_name='Upload')),
                ('phone_column', models.IntegerField(default=-1, verbose_name='Phone Column')),
                ('remarks', models.TextField(blank=True, default='', null=True, verbose_name='Remarks')),
            ],
            options={
                'verbose_name': 'upload',
                'verbose_name_plural': 'uploads',
            },
        ),
    ]
