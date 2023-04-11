from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_jwt.utils import jwt_decode_handler


def jwt_response_payload_handler(token, user=None, request=None):
    user_id = jwt_decode_handler(token)['user_id']
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    if user.is_doctor == True and user.is_hospital == False :
        return {'token': token, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/doctor-dashboard/'}
    elif user.is_patient == True:
        return {'token': token, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/patient-dashboard/'}
    elif user.is_doctor == True and user.is_hospital == True :
        return {'token': token, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/hospital-dashboard/'}
    elif user.is_superuser :
        return {'token': token, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/admin/'}