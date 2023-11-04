# Generated by Django 4.2.6 on 2023-11-01 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0018_category_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.AddField(
            model_name='task',
            name='category_color',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='task',
            name='category_title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]