# Generated by Django 4.2 on 2023-04-30 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='company',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
