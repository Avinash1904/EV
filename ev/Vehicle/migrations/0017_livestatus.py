# Generated by Django 3.2.9 on 2022-02-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vehicle', '0016_vehicle_vin_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_uid', models.CharField(blank=True, max_length=64, null=True)),
                ('data_capture_time', models.CharField(max_length=50, verbose_name='data capture time (yyyy-mm-dd-hh)')),
                ('latitude', models.CharField(max_length=15, verbose_name='device lat')),
                ('longitude', models.CharField(max_length=15, verbose_name='device long')),
                ('device_id', models.CharField(max_length=100)),
                ('speed', models.CharField(max_length=100)),
                ('account_id', models.CharField(max_length=50)),
                ('engine_state', models.CharField(max_length=5)),
                ('battery_voltage', models.CharField(max_length=10)),
            ],
        ),
    ]