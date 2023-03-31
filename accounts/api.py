from rest_framework.response import Response
from rest_auth.registration.views import RegisterView
from rest_framework import generics, permissions
from .models import Hospital
from .serializers import PatientSignUpSerializer ,DoctorRegisterationSerializer 
from rest_framework.decorators import api_view


class PatientRegisterApi(RegisterView):
    serializer_class = PatientSignUpSerializer  

class DoctorRegisterationApi(RegisterView):
    serializer_class = DoctorRegisterationSerializer 





