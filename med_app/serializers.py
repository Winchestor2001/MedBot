from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import *
from .utils import count_ratings


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id", "username", "is_doctor")


class DateSerializer(ModelSerializer):

    class Meta:
        model = Date
        fields = "__all__"


class DoctorRatingSerializer(ModelSerializer):

    class Meta:
        model = DoctorRating
        fields = "__all__"


class DoctorSerializer(ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'

    @staticmethod
    def get_doctor_date(obj):
        i = DateSerializer(data=obj.date_set.all(), many=True)

        i.is_valid()
        return i.data

    @staticmethod
    def count_doctor_rating(obj):
        ratings = DoctorRating.objects.filter(doctor=obj)
        result = count_ratings(ratings)
        return result

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        redata['date'] = [item['time_interval'] for item in self.get_doctor_date(instance)]
        redata['rating'] = self.count_doctor_rating(instance)
        return redata


class PatientSerializer(ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Patient
        fields = "__all__"


class PatientResultSerializer(ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = PatientResult
        exclude = ('doctor',)


class ChatSerializer(ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = ChatStorage
        fields = '__all__'


class ChatDoctorSerializer(ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


class ChatPatientSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = '__all__'


class ChatHistorySerializer(ModelSerializer):
    sender = SerializerMethodField()
    receiver = SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = '__all__'

    def get_user_obj(self, user_id):
        try:
            patient = Patient.objects.get(id=user_id)
            patient_obj = PatientSerializer(patient).data
            return {"id": patient_obj['id'], "full_name": patient_obj['full_name']}
        except Patient.DoesNotExist:
            pass

        try:
            doctor = Doctor.objects.get(id=user_id)
            doctor_obj = DoctorSerializer(doctor).data
            return {"id": doctor_obj['id'], "full_name": doctor_obj['full_name']}
        except Doctor.DoesNotExist:
            pass

        return None

    def get_sender(self, obj):
        return self.get_user_obj(obj.sender)

    def get_receiver(self, obj):
        return self.get_user_obj(obj.receiver)

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        if redata['image']:
            redata['image_bytes'] = '/' + redata['image'].split('/', 3)[-1]
            redata.pop('image')
        return redata

