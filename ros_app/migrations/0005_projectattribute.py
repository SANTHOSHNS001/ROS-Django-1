# Generated by Django 4.2.6 on 2023-10-17 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ros_app', '0004_alter_vdmldocumentdetail_actual_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=255)),
                ('field_type', models.CharField(max_length=50)),
                ('choices', models.TextField(blank=True, null=True)),
                ('required', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='ros_app.projects')),
            ],
        ),
    ]
