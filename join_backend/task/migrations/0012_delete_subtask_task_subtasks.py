# Generated by Django 4.2.6 on 2023-10-30 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_subtask_delete_customuserandcontact_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subtask',
        ),
        migrations.AddField(
            model_name='task',
            name='subtasks',
            field=models.JSONField(default=dict),
        ),
    ]
