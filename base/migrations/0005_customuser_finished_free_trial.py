# Generated by Django 3.1.3 on 2022-03-02 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_customuser_expiry_free_trial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='finished_free_trial',
            field=models.BooleanField(default=False),
        ),
    ]