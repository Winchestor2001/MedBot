from .views import *
from django.urls import path


urlpatterns = [
    path("user/", UserApiView.as_view()),
    path("doctor/", DoctorApiView.as_view()),
    path("doctor_info/", DoctorInfoApiView.as_view()),
    path("doctor_work_time/", GetDoctorCorrectDatesAPIView.as_view()),
    path("patient/", PatientApiView.as_view()),
    path("single_   patient/", SinglePatientApiView.as_view()),
    path("patient_result/", PatientResultApiView.as_view()),
]
