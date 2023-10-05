# Generated by Django 4.2.6 on 2023-10-05 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ros_app', '0003_rename_username_customroles_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Custom User', 'verbose_name_plural': 'Custom Users'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(help_text='Enter a unique email address.', max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(help_text="Enter the user's first name.", max_length=30, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(help_text="Enter the user's last name.", max_length=30, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, help_text='Upload a profile picture for the user.', null=True, upload_to='user_pictures/', verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(blank=True, help_text='Assign a role to the user.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='ros_app.customroles', verbose_name='Role'),
        ),
    ]