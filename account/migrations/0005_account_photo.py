# Generated by Django 4.1.3 on 2022-11-19 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_pass_phrase'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photo'),
        ),
    ]
