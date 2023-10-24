from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "is_doctor")


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["user", "full_name", "direction", "price", "experience", "services", "reviews", "busy"]


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"