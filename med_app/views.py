from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


class UserApiView(APIView):
    def get(self, request):
        data = User.objects.all()
        return Response({"Users": UserSerializer(data, many=True).data})

    def post(self, request):
        new_user = User.objects.update_or_create(
            user_id=request.data["user_id"],
            username=request.data["username"]
        )
        return Response({"post": model_to_dict(new_user[0])})


class DoctorApiView(APIView):
    def get(self, request):
        data = Doctor.objects.all()
        return Response({"Doctors": DoctorSerializer(data, many=True).data})


class PatientApiView(APIView):
    def get(self, request):
        data = Patient.objects.all().values()
        return Response({"Patient": PatientSerializer(data, many=True).data})

    def post(self, request):
        new_patient = Patient.objects.update_or_create(
            user=request.data["user"],
            full_name=request.data["fullname"],
            phone_number=request.data["phone_number"],
            additional_information=request.data["additional_information"],
            doctor=request.data["doctor"],
            confirance_date=request.data["confirence_date"]
        )
        return Response({"New Patient": model_to_dict(new_patient)})


class PatientResultApiView(APIView):
    def get(self, request):
        user = request.data["user"],
        patient = Patient.objects.get(user__user_id=user)
        patient_results = PatientResult.objects.filter(patient=patient)

        serializer = PatientResultSerializer(data=patient_results, many=True)
        serializer.is_valid()
        return Response({'data': serializer.data})


