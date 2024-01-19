from .views import *
from django.urls import path


urlpatterns = [
    path("user/", UserApiView.as_view()),
    path("doctor/", DoctorApiView.as_view()),
    path("doctor_info/", DoctorInfoApiView.as_view()),
    path("doctor_work_time/", GetDoctorCorrectDatesAPIView.as_view()),
    path("end_record/", EndRecordAPIView.as_view()),
    path("patient/", PatientApiView.as_view()),
    path("single_patient/", SinglePatientApiView.as_view()),
    path("patient_result/", PatientResultApiView.as_view()),
    path("patient_result_pdf/", GetPatientResultPDF.as_view()),
    path("call/", DoctorCallAPIView.as_view()),
    path("admins_list/", GetAdminsIdAPIView.as_view()),
    path("doctor_rating/", DoctorRatingAPIView.as_view()),
    path("withdraw/", WithDrawDoctorAPI.as_view()),

    path("video_stream_doctor/<str:room_name>/", VideoStreamDoctorView.as_view()),
    path("video_stream_patient/<str:room_name>/", VideoStreamPatientView.as_view()),

    path('payment_notification/', PaymentNotification.as_view()),

    path('doctor_chats/', GetDoctorChatsAPI.as_view()),
    path('doctor_about/', AboutDoctorAPI.as_view()),
    path('chat_history/', GetChatHistoryAPI.as_view()),
]
