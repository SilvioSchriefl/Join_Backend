# Generated by Django 4.2.6 on 2023-10-30 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assignee',
        ),
    ]