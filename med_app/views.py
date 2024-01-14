import os
from django.forms import model_to_dict
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, get_object_or_404

from core.settings import env
from .payment_system import create_invoice
from .serializers import *
from .models import *
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from bot.data.config import BOT_TOKEN
from .utils import check_dates, filter_doctor_direction, send_message, modify_date_type, generate_room_code, \
    create_hash, send_message_with_web_app, create_pdf, save_recorded_video
from .yasg_schame import doctor_get_schame, patient_get_param, doctor_post_schame, patient_post_param, \
    doctor_times_get_param, doctor_times_get_schame, patient_result_post_param, doctor_get_param, \
    single_patient_get_param, doctor_call_post_param, doctor_rating_post_param, doctor_rating_post_param2
import logging
from django.views import View
import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse

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
            user = User.objects.get(user_id=request.data["user_id"])
            return Response({"user": model_to_dict(user)}, status=200)


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
        doctor = get_object_or_404(Doctor, activate_url__contains=activate_code)
        is_doc = True

        user, created = User.objects.get_or_create(
            user_id=user_id,
            defaults={
                'username': username,
                'is_doctor': is_doc,
            }
        )

        if not created:
            user.is_doctor = is_doc
            user.save()

        doctor.user = user
        doctor.save()

        return Response({"user": model_to_dict(user)})


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
        current_year = datetime.now().astimezone(timezone.pytz.timezone('Asia/Tashkent')).year
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
        pay_url, bill_id = create_invoice(str(new_patient.doctor.price))

        PatientPayment.objects.create(
            patient=new_patient,
            doctor=new_patient.doctor,
            bill_id=bill_id,
            amount=new_patient.doctor.price
        )

        return Response({"patient": model_to_dict(new_patient), "pay_invoice": pay_url})


class PatientResultApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Get patient result information (bot)",
        operation_description="This returns patient result information",
        manual_parameters=[patient_get_param]

    )
    def get(self, request):
        user = request.data["user"]
        patient = PatientResult.objects.filter(patient_id__user_id=user)
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


class GetPatientResultPDF(APIView):
    def get(self, request):

        patient = request.data["patient"]
        try:
            result = PatientResult.objects.get(id=patient)
        except:
            return Response({"patient_result": "There no result belong this ID"})

        p = f"{result.patient.full_name}_{result.id}"
        output_path = f"./media/pdf_results/{p}.pdf"
        exist = os.path.exists(output_path)
        if not exist:
            create_pdf(result, output_path)
        url = f"{env.str('API_URL')}/media/pdf_results/{p}.pdf"
        return Response({"patient_result_pdf": url})


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


class DoctorCallAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Doctor call to patient (web)",
        manual_parameters=doctor_call_post_param
    )
    def post(self, request):
        doctor = request.data["doctor_id"]
        patient = request.data["patient_id"]
        data_type = request.data["type"]
        meet = MeetingRoom.objects.get(patient__id=patient)
        hash_data = create_hash(
            {"doctor": doctor, "patient": patient, "type": data_type}
        )
        webapp_url = f"{env.str('UI_DOMEN')}/meeting/{meet.meet_code}/{hash_data}"
        send_message_with_web_app(
            user_id=meet.patient.user.user_id,
            url=webapp_url,
            message="Soon meet start",
        )

        return Response({"Call": "wait"})


class ChatAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Chat (web)",
        manual_parameters=doctor_call_post_param
    )
    def post(self, request):
        doctor = request.data["doctor_id"]
        patient = request.data["patient_id"]
        data_type = request.data["type"]
        meet = MeetingRoom.objects.get(patient__id=patient)
        hash_data = create_hash(
            {"doctor": doctor, "patient": patient, "type": data_type}
        )
        webapp_url = f"{env.str('UI_DOMEN')}/meeting/{meet.meet_code}/{hash_data}"
        send_message_with_web_app(
            user_id=meet.patient.user.user_id,
            url=webapp_url,
            message="Soon meet start",
        )

        return Response({"Call": "wait"})


class GetAdminsIdAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="Get Admins ID (bot)",
        operation_description="This returns admins id",

    )
    def get(self, request):
        admins = BotAdmin.objects.all()
        data = [item.user.user_id for item in admins]
        return Response({"admins": data})


class DoctorRatingAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Doctor rating (web)",
        request_body=doctor_rating_post_param2
    )
    def post(self, request):
        doctor = Doctor.objects.get(id=request.data["doctor_id"])
        rating = request.data["rating"]
        DoctorRating.objects.create(
            doctor=doctor, rating=rating
        )

        return Response({"status": "OK"}, status=201)


class EndRecordAPIView(APIView):
    def get(self, request):
        room_name = request.GET.get('room_name')
        save_recorded_video(
            f"{room_name}_1.webm", f"{room_name}_2.webm", f"recorded_{room_name}.webm"
        )
        return Response({"status": "OK"}, status=200)


class VideoStreamDoctorView(View):
    def get(self, request, room_name):
        current_direction = os.getcwd()
        video_path = f"{current_direction}/media/{room_name}_1.webm"

        content_type, _ = guess_type(video_path)
        content_type = content_type or 'application/octet-stream'

        video_file = open(video_path, 'rb')
        file_wrapper = FileWrapper(video_file)

        response = StreamingHttpResponse(file_wrapper, content_type=content_type)

        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_path)}"'

        return response


class VideoStreamPatientView(View):
    def get(self, request, room_name):
        current_direction = os.getcwd()
        video_path = f"{current_direction}/media/{room_name}_2.webm"

        content_type, _ = guess_type(video_path)
        content_type = content_type or 'application/octet-stream'

        video_file = open(video_path, 'rb')
        file_wrapper = FileWrapper(video_file)

        response = StreamingHttpResponse(file_wrapper, content_type=content_type)

        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_path)}"'

        return response


class PaymentNotification(APIView):
    def post(self, request):
        print(request.data)

        return Response({"status": "received"}, status=200)

