# Generated by Django 4.2.6 on 2023-10-23 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='color',
            field=models.CharField(blank=True, default='#00000', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='initials',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
