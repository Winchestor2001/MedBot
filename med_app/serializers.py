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


class PatientChatSerializer(ModelSerializer):
    doctor = DoctorSerializer()
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

    class Meta:
        model = ChatMessage
        fields = '__all__'

    def get_user_obj(self, obj):
        if obj.type == 'patient':
            patient = Patient.objects.get(id=obj.sender)
            patient_obj = PatientSerializer(patient).data

            doctor = Doctor.objects.get(id=obj.receiver)
            doctor_obj = DoctorSerializer(doctor).data

            confirance_status = patient.confirance_status
            patient = {"id": patient_obj['id'], "full_name": patient_obj['full_name']}
            doctor = {"id": doctor_obj['id'], "full_name": doctor_obj['full_name']}
            return patient, doctor, confirance_status

        elif obj.type == 'doctor':
            doctor = Doctor.objects.get(id=obj.sender)
            doctor_obj = DoctorSerializer(doctor).data

            patient = Patient.objects.get(id=obj.receiver)
            patient_obj = PatientSerializer(patient).data

            confirance_status = patient.confirance_status
            patient = {"id": patient_obj['id'], "full_name": patient_obj['full_name']}
            doctor = {"id": doctor_obj['id'], "full_name": doctor_obj['full_name']}
            return doctor, patient, confirance_status

    def to_representation(self, instance):
        redata = super().to_representation(instance)
        if redata['image']:
            redata['image_bytes'] = '/' + redata['image'].split('/', 3)[-1]
            redata.pop('image')

        redata['sender'], redata['receiver'], redata['status'] = self.get_user_obj(instance)

        return redata

