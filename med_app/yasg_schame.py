from drf_yasg import openapi


doctor_get_schame = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'activate_code': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['user_id', 'username', 'activate_code']
)

doctor_post_schame = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'doctor': openapi.Schema(type=openapi.TYPE_OBJECT),
        'activate_code': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['user_id', 'username', 'activate_code']
)

patient_param = openapi.Parameter(
    name='user',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER,
    description='User telegram id',
    required=True
)

