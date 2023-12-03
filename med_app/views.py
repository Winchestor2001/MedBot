from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from .serializers import *
from .models import *
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from bot.data.config import BOT_TOKEN
from .utils import check_dates, filter_doctor_direction, send_message, modify_date_type, generate_room_code
from .yasg_schame import doctor_get_schame, patient_get_param, doctor_post_schame, patient_post_param, \
    doctor_times_get_param, doctor_times_get_schame, patient_result_post_param, doctor_get_param, \
    single_patient_get_param
import logging

logger = logging.getLogger(__name__)


class UserApiView(APIView):
    def get(self, request):
        data = User.objects.all()
        return Response({"users": UserSerializer(data, many=True).data})

    def post(self, request):
        serializer = UserSerializer(
            data={
                "user_id": request.data["user_id"],
                "username": request.data["username"],
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=201)
        else:
            return Response({"user": "Alredy created"}, status=200)


class DoctorInfoApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Get doctor information (web)",
        operation_description="This returns doctor information",
        manual_parameters=[doctor_get_param]
    )
    def get(self, request):
        data = Doctor.objects.get(pk=request.GET["doctor_id"])
        serializer = DoctorSerializer(instance=data)
        return Response({"doctors": serializer.data})


class DoctorApiView(APIView):

    @swagger_auto_schema(
        operation_summary="Get doctors list (web)",
        responses={200: doctor_post_schame}
    )
    def get(self, request):
        data = Doctor.objects.all()
        directions = filter_doctor_direction(data)
        return Response({"doctors": DoctorSerializer(data, many=True).data, "directions": directions})

    @swagger_auto_schema(
        operation_summary="Create doctor (bot)",
        request_body=doctor_get_schame
    )
    def post(self, request):
        user_id = request.data["user_id"]
        username = request.data["username"]
        activate_code = request.data["activate_code"]
        doctor = Doctor.objects.filter(activate_url__contains=activate_code)
        if doctor.exists():
            is_doc = True
        else:
            is_doc = False

        user = User.objects.filter(user_id=user_id)
        if user.exists():
            user[0].is_doctor = is_doc
            user[0].save()
        else:
            user = User.objects.create(
                user_id=user_id,
                username=username,
                is_doctor=is_doc,
            )
        return Response({"user": model_to_dict(user[0])})


class SinglePatientApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Get single patient information (web)",
        operation_description="This return patient information",
        manual_parameters=[single_patient_get_param]

    )
    def get(self, request):
        patient = Patient.objects.filter(id=request.GET["patient_id"])
        if patient.exists():
            serializer = PatientSerializer(instance=patient[0])
            return Response({"patient": serializer.data})
        else:
            return Response({"patient": "No Exists"}, status=403)


class PatientApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Get patient information (bot/web)",
        operation_description="This returns patient information",
        manual_parameters=[patient_get_param]

    )
    def get(self, request):
        user = User.objects.get(user_id=request.GET["user"])
        data = Patient.objects.filter(user=user)
        serializer = PatientSerializer(instance=data, many=True)
        return Response({"patient": serializer.data})

    @swagger_auto_schema(
        operation_summary="Create new patient (web)",
        request_body=patient_post_param
    )
    def post(self, request):
        selected_date = request.data['conference_date']["selectedDate"]
        selected_time = request.data['conference_date']["selectedTime"]
        selected_month = request.data['conference_date']["selectedMonth"]
        start_time_str = selected_time.split(' - ')[0].strip()

        formatted_datetime_str = f"{selected_month:02d}-{selected_date:02d} {start_time_str}"
        formatted_datetime = datetime.strptime(formatted_datetime_str, "%m-%d %H:%M")

        new_patient = Patient.objects.create(
            user=User.objects.get(user_id=request.data["user"]),
            full_name=request.data["full_name"],
            phone_number=request.data["phone_number"],
            additional_information=request.data["additional_information"],
            doctor=Doctor.objects.get(id=request.data["doctor_id"]),
            confirance_date=formatted_datetime,
        )
        current_year = datetime.now().year
        formatted_datetime = formatted_datetime.replace(year=current_year)
        MeetingRoom.objects.create(
            patient=new_patient,
            doctor=new_patient.doctor,
            start_meet_date=formatted_datetime,
            meet_code=generate_room_code()
        )

        data = model_to_dict(new_patient)
        get_doctor = new_patient.doctor
        date = modify_date_type(str(data["confirance_date"]))
        msg = f"🎉 Поздравляем! Ваше бронирование подтверждено.🎉\n\n" \
              f"📋 Заказ ID: {data['id']}\n" \
              f"👨‍⚕️ Доктор: {get_doctor}\n" \
              f"📆 Дата и время: {date}\n\n" \
              f"Спасибо, что выбрали наш сервис! Если у вас есть какие-либо вопросы или вам нужно перенести встречу, " \
              f"свяжитесь с нами. 📞"
        user_id = int(request.data["user"])
        send_message(BOT_TOKEN, user_id, msg)
        return Response({"patient": model_to_dict(new_patient)})


class PatientResultApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Get patient result information (bot)",
        operation_description="This returns patient result information",
        manual_parameters=[patient_get_param]

    )
    def get(self, request):
        user = request.data["user"]
        patient = Patient.objects.filter(user__user_id=user)
        serializer = PatientResultSerializer(data=patient, many=True)
        serializer.is_valid()
        return Response({'patient_results': serializer.data})

    @swagger_auto_schema(
        operation_summary="Create patient result (web)",
        request_body=patient_result_post_param
    )
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


class GetDoctorCorrectDatesAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Correct Dates (web)",
        operation_description="This returns doctor work time information",
        manual_parameters=doctor_times_get_param,
        responses={200: doctor_times_get_schame}

    )
    def get(self, request):
        user = Patient.objects.filter(user=User.objects.get(user_id=request.GET.get('user')))
        doctor = Doctor.objects.get(pk=request.GET.get('doctor'))
        month = request.GET.get('month')
        day = request.GET.get('day')
        result = check_dates(user, doctor, month, day)

        return Response({"STATUS": "OK", "correct_date": result})
