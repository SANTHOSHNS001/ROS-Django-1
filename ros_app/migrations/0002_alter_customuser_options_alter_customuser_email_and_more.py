# Generated by Django 4.2.6 on 2023-10-11 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ros_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('ros_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=ros_app.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='users', to='ros_app.projects'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='ros_app.customroles'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='vdml_documents',
            field=models.ManyToManyField(blank=True, related_name='users', to='ros_app.vdml_document'),
        ),
        migrations.AlterField(
            model_name='vdmldocumentdetail',
            name='ros_engineer',
            field=models.ManyToManyField(blank=True, related_name='ros_engineer', to=settings.AUTH_USER_MODEL),
        ),
    ]
