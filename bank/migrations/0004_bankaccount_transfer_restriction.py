# Generated by Django 4.1.3 on 2022-11-17 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_bankaccount_transfer_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='transfer_restriction',
            field=models.CharField(blank=True, default='None', max_length=25, null=True),
        ),
    ]
