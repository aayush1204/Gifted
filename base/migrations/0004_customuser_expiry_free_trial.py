# Generated by Django 3.1.3 on 2022-03-02 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20220302_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='expiry_free_trial',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]