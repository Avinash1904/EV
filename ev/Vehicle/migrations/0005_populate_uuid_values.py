# Generated by Django 3.2.9 on 2022-02-06 12:22

from django.db import migrations, models
import uuid


def gen_uuid_device(apps, schema_editor):
    MyModel = apps.get_model('Vehicle', 'Device')
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


def gen_uuid_battery(apps, schema_editor):
    MyModel = apps.get_model('Vehicle', 'Battery')
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


def gen_uuid_vehicle(apps, schema_editor):
    MyModel = apps.get_model('Vehicle', 'Vehicle')
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('Vehicle', '0004_auto_20220206_1922'),
    ]

    operations = [
        migrations.RunPython(
            gen_uuid_battery, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(
            gen_uuid_device, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(
            gen_uuid_vehicle, reverse_code=migrations.RunPython.noop),
    ]
