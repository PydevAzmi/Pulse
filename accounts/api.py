from datetime import datetime
from urllib import response
from rest_framework_jwt.views import ObtainJSONWebToken 
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_auth.registration.views import RegisterView 
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.utils import jwt_response_payload_handler
from .serializers import PatientSignUpSerializer ,DoctorRegisterationSerializer ,LoginJWTSerializer
from rest_framework_jwt.settings import api_settings

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
            response = Response(payload)
            response.set_cookie(key='jwt', value=response, httponly=True, max_age=86400)

            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                            api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)

            return Response(payload)
        return Response(serializer.errors)
    

class LogoutView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Delete the token associated with the user
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)