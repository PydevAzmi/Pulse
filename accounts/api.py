from datetime import datetime
from rest_framework_jwt.views import ObtainJSONWebToken 
from accounts.utils import jwt_response_payload_handler
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_auth.registration.views import RegisterView 
from rest_framework import permissions  
from rest_framework.response import Response
from rest_framework import status, views
from django.contrib.auth import logout,login
from rest_framework.views import APIView 
from .serializers import LoginSerializer, PatientSignUpSerializer ,DoctorRegisterationSerializer 



class PatientRegisterApi(RegisterView):
    serializer_class = PatientSignUpSerializer

class DoctorRegisterationApi(RegisterView):
    serializer_class = DoctorRegisterationSerializer

class LoginViewApi(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        if user.is_doctor == True and user.is_hospital == False :
            return Response({'token': token.key, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/doctor-dashboard/'}, status=status.HTTP_202_ACCEPTED)
        elif user.is_patient == True:
            return Response({'token': token.key, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/patient-dashboard/'}, status=status.HTTP_202_ACCEPTED)
        elif user.is_doctor == True and user.is_hospital == True :
            return Response({'token': token.key, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/hospital-dashboard/'}, status=status.HTTP_202_ACCEPTED)
        elif user.is_superuser :
            return Response({'token': token.key, 'user': {'id': user.id, 'username': user.username}, 'redirect_to': '/admin/'}, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # Delete the token associated with the user
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully',status=status.HTTP_204_NO_CONTENT)
























'''
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
'''    
