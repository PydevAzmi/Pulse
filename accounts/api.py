from rest_framework.response import Response
from rest_auth.registration.views import RegisterView 
from rest_framework import permissions

from accounts.views import logout
from .serializers import PatientSignUpSerializer ,DoctorRegisterationSerializer 
from rest_framework.decorators import api_view ,permission_classes

from rest_framework_jwt.views import ObtainJSONWebToken
from .serializers import LoginJWTSerializer


class PatientRegisterApi(RegisterView):
    serializer_class = PatientSignUpSerializer

class DoctorRegisterationApi(RegisterView):
    serializer_class = DoctorRegisterationSerializer
    permission_classes = [permissions.AllowAny] 


class ObtainJWTLoginViewApi(ObtainJSONWebToken):
    serializer_class = LoginJWTSerializer


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')