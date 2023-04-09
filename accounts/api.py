from rest_auth.registration.views import RegisterView 
from rest_framework import permissions

from accounts.views import logout
from .serializers import PatientSignUpSerializer ,DoctorRegisterationSerializer 
from rest_framework.decorators import api_view ,permission_classes

from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import LoginJWTSerializer
from accounts.utils import jwt_response_payload_handler
from rest_framework.response import Response
from rest_framework import status


class PatientRegisterApi(RegisterView):
    serializer_class = PatientSignUpSerializer

class DoctorRegisterationApi(RegisterView):
    serializer_class = DoctorRegisterationSerializer

class ObtainJWTLoginViewApi(ObtainJSONWebToken):
    serializer_class = LoginJWTSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            payload = jwt_response_payload_handler(token, user, request)
            return Response(payload)
        return Response(serializer.errors)
           


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')