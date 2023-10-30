from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "is_doctor")


class DateSerializer(ModelSerializer):

    class Meta:
        model = Date
        fields = ('work_time',)


class DoctorSerializer(ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'

    @staticmethod
    def get_doctor_date(obj):
        i = DateSerializer(data=obj.date_set.all(), many=True)

        i.is_valid()
        return i.data

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['work_time'] = [item['work_time'] for item in self.get_doctor_date(instance)]
        return redata


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class PatientResultSerializer(ModelSerializer):
    class Meta:
        model = PatientResult
        fields = "__all__"
