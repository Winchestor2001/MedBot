from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from datetime import datetime


class UserApiView(APIView):
    def get(self, request):
        data = User.objects.all()
        return Response({"Users": UserSerializer(data, many=True).data})

    def post(self, request):
        new_user = User.objects.get_or_create(
            user_id=request.data["user_id"],
            username=request.data["username"]
        )
        return Response({"post": model_to_dict(new_user)})


class DoctorApiView(APIView):
    def get(self, request):
        data = Doctor.objects.all()
        return Response({"Doctors": DoctorSerializer(data, many=True).data})

    def post(self, request):
        user_id = request.data["user_id"]
        username = request.data["username"]
        activate_code = request.data["activate_code"]
        doctor = Doctor.objects.filter(activate_code__contains=activate_code).exists()
        if doctor:
            is_doc = True
        else:
            is_doc = False

        new_user = User.objects.get_or_create(
            user_id=user_id,
            username=username,
            is_doctor=is_doc,
        )
        return Response({"post": model_to_dict(new_user)})


class PatientApiView(APIView):
    def get(self, request):
        user = User.objects.get(user_id=request.data["user"])
        data = Patient.objects.filter(user=user)
        return Response({"Patient": PatientSerializer(data, many=True).data})

    def post(self, request):
        new_patient = Patient.objects.create(
            user=User.objects.get(user_id=request.data["user"]),
            full_name=request.data["fullname"],
            phone_number=request.data["phone_number"],
            additional_information=request.data["additional_information"],
            doctor=Doctor.objects.get(id=request.data["doctor"]),
            confirance_date=datetime.strptime(request.data["confirence_date"], '%Y-%m-%d %H:%M'),
        )
        return Response({"New Patient": model_to_dict(new_patient)})


class PatientResultApiView(APIView):
    def get(self, request):
        user = request.data["user"]
        patient = Patient.objects.filter(user__user_id=user)
        serializer = PatientResultSerializer(data=patient, many=True)
        serializer.is_valid()
        return Response({'data': serializer.data})

    def post(self, request):
        patient = Patient.objects.get(id=request.data["patient"])
        doctor = Doctor.objects.get(id=request.data["doctor"])
        result_text = request.data["result_text"]

        patient_result = PatientResult.objects.create(
            patient=patient,
            doctor=doctor,
            result_text=result_text
        )

        return Response({"Patient result": model_to_dict(patient_result)})


