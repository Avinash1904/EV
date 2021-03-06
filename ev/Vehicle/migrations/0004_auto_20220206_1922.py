# Generated by Django 3.2.9 on 2022-02-06 12:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Vehicle', '0003_auto_20220129_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='battery',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, null=True, verbose_name='UUID'),
        ),
        migrations.AddField(
            model_name='device',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, null=True, verbose_name='UUID'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, null=True, verbose_name='UUID'),
        ),
    ]
