# Generated by Django 3.1.1 on 2020-10-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_auto_20201003_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='usuarios'),
        ),
    ]
