# Generated by Django 4.2.6 on 2023-10-05 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ros_app', '0002_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
    ]
