import datetime

from django.db import models
from uuid import uuid4
from bot.data.config import BOT_URL
from ckeditor_uploader.fields import RichTextUploadingField


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
    about = RichTextUploadingField(blank=True, null=True)
    balance = models.IntegerField(default=0)
    activate_url = models.CharField(max_length=100, default='null')

    def __str__(self):
        return self.full_name

    def save(self, **kwargs):
        self.activate_url = BOT_URL + "?start=" + uuid4().hex[:8]
        return super().save(**kwargs)


class Date(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    time_interval = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.doctor)


class Patient(models.Model):
    CONFIRANCE_STASTUS = (
        ('wait', 'wait'),
        ('close', 'close'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=255)
    additional_information = models.TextField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    confirance_date = models.DateField(default=None)
    confirance_time = models.CharField(max_length=50, blank=True, null=True)
    confirance_status = models.CharField(max_length=20, choices=CONFIRANCE_STASTUS, default='wait')

    def __str__(self):
        return self.full_name


class PatientResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    result_text = models.TextField()

    def __str__(self):
        return str(self.patient)


class MeetingRoom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_meet_date = models.DateTimeField(blank=True, null=True)
    meet_code = models.CharField(max_length=100)

    def __str__(self):
        return str(self.patient)


class BotAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class DoctorRating(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return str(self.doctor)


class ChatStorage(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField()
    chat_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor} - {self.patient}"


class PatientPayment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    bill_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"

