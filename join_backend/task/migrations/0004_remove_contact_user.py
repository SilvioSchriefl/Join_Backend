# Generated by Django 4.2.6 on 2023-10-27 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
    ]
