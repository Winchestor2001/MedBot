from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "is_doctor")


class ServiceSerializer(ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    # def get_children(self, obj):
    #     # print(obj.date_set.all())
    #     i = ServiceSerializer(data=obj.date_set.all(), many=True)
    #     print(i)
    #     i.is_valid()
    #
    #     return i.data
    #
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #
    #     if self.get_children(instance):
    #         ret['children'] = self.get_children(instance)
    #     return ret


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"