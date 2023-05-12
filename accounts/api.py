from .models import User ,Doctor,Patient, Hospital
from consultation.models import Survey,Report,Review
from consultation.serializers import SurveyReadSerializer
from .permssions import IsDoctorOrReadOnly ,IsPatientOrReadOnly
from rest_framework.authtoken.models import Token
from rest_auth.registration.views import RegisterView 
from rest_framework import permissions ,viewsets
from rest_framework.response import Response
from rest_framework import status, views, generics
from django.contrib.auth import logout,login
from rest_framework.views import APIView 
from .serializers import (  LoginSerializer,
                            PatientSignUpSerializer ,
                            DoctorRegisterationSerializer,
                            DoctorSerializer,
                            PatientSerializer,
                            UserUpdateSerializer,
                            HospitalAdminSignUpSerializer)



class PatientRegisterApi(RegisterView):
    serializer_class = PatientSignUpSerializer

class DoctorRegisterationApi(RegisterView):
    serializer_class = DoctorRegisterationSerializer

class HospitalAdminRegisterApi(RegisterView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = HospitalAdminSignUpSerializer

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

class DoctorApi(viewsets.ModelViewSet):
    queryset = Doctor.objects.all( )
    serializer_class = DoctorSerializer
    

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return UserUpdateSerializer
        return DoctorSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated , permissions.IsAdminUser)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsDoctorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
    
    '''
    filter_backends = [UserFilterBackend, DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['author']
    '''

## doctor Profile & Dashboard
class DoctorProfileViewSet(viewsets.ModelViewSet,):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctorOrReadOnly]
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated , permissions.IsAdminUser)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsDoctorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_doctor:
            return Doctor.objects.filter(user=user).select_related('user','hospital','review')
                    
        else:
            return Doctor.objects.none()

## patient Profile
class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsPatientOrReadOnly]
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated , permissions.IsAdminUser)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsPatientOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_patient:
            return Patient.objects.filter(user=user).select_related('user')
                    
        else:
            return Patient.objects.none()

class PatientSurveyList(generics.RetrieveAPIView):
    serializer_class = SurveyReadSerializer
    queryset = Survey.objects.all()

class DoctorListViewSet(viewsets.ModelViewSet,):
    queryset = Doctor.objects.select_related('user','hospital','review')
    serializer_class = DoctorSerializer
    permission_classes = [IsPatientOrReadOnly]
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated , permissions.IsAdminUser)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
    

 




"""
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .models import Model1, Model2
from .serializers import Model1Serializer, Model2Serializer

class MultiModelViewSet(viewsets.GenericViewSet,
                        generics.ListAPIView,
                        generics.CreateAPIView,
                        generics.RetrieveAPIView,
                        generics.UpdateAPIView,
                        generics.DestroyAPIView):
    queryset = Model1.objects.all()
    serializer_class = Model1Serializer
    lookup_field = 'pk'

    def get_queryset(self):
        if self.kwargs.get('model') == 'model1':
            self.queryset = Model1.objects.all()
            self.serializer_class = Model1Serializer
        elif self.kwargs.get('model') == 'model2':
            self.queryset = Model2.objects.all()
            self.serializer_class = Model2Serializer
        else:
            self.queryset = None
            self.serializer_class = None
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'detail': 'Invalid model specified'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'detail': 'Invalid model specified'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'detail': 'Invalid model specified'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'detail': 'Invalid model specified'}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
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
