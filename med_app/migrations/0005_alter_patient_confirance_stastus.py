# Generated by Django 4.2.6 on 2023-11-03 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_app', '0004_remove_patient_doctor_patient_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='confirance_stastus',
            field=models.CharField(choices=[('wait', 'wait'), ('close', 'close')], default='wait', max_length=20),
        ),
    ]