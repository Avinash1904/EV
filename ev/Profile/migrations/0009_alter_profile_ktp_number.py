# Generated by Django 3.2.9 on 2022-01-27 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_rename_uid_profile_ktp_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ktp_number',
            field=models.CharField(max_length=100, verbose_name='KTP Number'),
        ),
    ]
