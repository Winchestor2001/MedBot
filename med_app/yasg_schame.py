from drf_yasg import openapi
from .serializers import DoctorSerializer, PatientSerializer

doctor_get_schame = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'activate_code': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['user_id', 'username', 'activate_code']
)

doctor_post_schame = openapi.Response(
    description="You get a json:",
    schema=DoctorSerializer
)

patient_get_param = openapi.Parameter(
    name='user',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description='User telegram id',
    required=True
)

doctor_get_param = openapi.Parameter(
    name='doctor_id',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description='Doctor id',
    required=True
)

patient_post_param = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'full_name': openapi.Schema(type=openapi.TYPE_STRING),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
        'additional_information': openapi.Schema(type=openapi.TYPE_STRING),
        'doctor_id': openapi.Schema(type=openapi.TYPE_STRING),
        'confirance_date': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['user_id', 'full_name', 'phone_number', 'additional_information', 'doctor_id', 'confirance_date']
)

patient_result_post_param = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'patient': openapi.Schema(type=openapi.TYPE_INTEGER),
        'doctor': openapi.Schema(type=openapi.TYPE_INTEGER),
        'result_text': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['patient', 'doctor', 'result_text']
)

doctor_times_get_param = [
    openapi.Parameter(
        name='user',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='User telegram id',
        required=True
    ),
    openapi.Parameter(
            name='doctor',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='Doctor id',
            required=True
        ),
    openapi.Parameter(
                name='date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Month number',
                required=True
            )
]

doctor_times_get_schame = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'work_time': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
    },
    required=['work_time']
)
