# Generated by Django 3.2.8 on 2021-11-15 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_alter_sales_followupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='followupnotes',
            name='followupdate',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]