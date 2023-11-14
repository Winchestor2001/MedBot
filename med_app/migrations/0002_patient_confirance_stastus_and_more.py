# Generated by Django 4.2.6 on 2023-11-02 06:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='confirance_stastus',
            field=models.CharField(choices=[('wait', 'wait'), ('end', 'end')], default='wait', max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='confirance_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 2, 11, 33, 13, 327741)),
        ),
    ]