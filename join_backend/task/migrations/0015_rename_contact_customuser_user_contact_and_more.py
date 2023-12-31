# Generated by Django 4.2.6 on 2023-10-31 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0014_contact_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='contact',
            new_name='user_contact',
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
