# Generated by Django 3.2.9 on 2022-02-07 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0012_remove_uuid_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Address'),
        ),
    ]