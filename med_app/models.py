import datetime

from django.db import models


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    is_doctor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=500)
    avatar = models.ImageField(upload_to='doctor_avatar/')
    direction = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    experience = models.TextField()
    services = models.TextField()
    reviews = models.IntegerField(default=0)
    busy = models.BooleanField(default=False)
    activate_code = models.IntegerField()

    def __str__(self):
        return self.full_name


class Date(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    work_time = models.DateTimeField()

    def __str__(self):
        return str(self.doctor)


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=255)
    additional_information = models.TextField(null=True)
    doctor = models.ManyToManyField(Doctor)
    confirance_date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.full_name


