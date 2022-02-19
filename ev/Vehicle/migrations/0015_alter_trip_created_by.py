# Generated by Django 3.2.9 on 2022-02-19 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0021_remove_profile_phone_number'),
        ('Vehicle', '0014_alter_trip_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='Profile.profile'),
        ),
    ]
