import json
from django.http import HttpResponse ,JsonResponse
from requests import Response
from rest_framework import serializers
from django.core.serializers import serialize
from rest_framework.authtoken.models import Token
from rest_auth.registration.serializers import RegisterSerializer
from django_countries.serializer_fields  import CountryField
from .models import Patient, Doctor ,Hospital
GENDER = {
    'Male': 'Male',
    'Female': 'Female'
} 

class PatientSignUpSerializer(RegisterSerializer):
    first_name = serializers.CharField( write_only=True, required=True,max_length = 50)
    last_name = serializers.CharField(max_length = 50)
    country = CountryField()
    gender = serializers.ChoiceField(choices=GENDER)
    Phone_number = serializers.CharField()
   
    def get_cleaned_data(self):
        data = super(PatientSignUpSerializer, self).get_cleaned_data()
        extra_data = {
                'first_name' : self.validated_data.get('first_name', ''),
                'last_name' : self.validated_data.get('last_name', ''),
                'Phone_number' : self.validated_data.get('Phone_number', ''),
                'country' : self.validated_data.get('country', ''),
                'gender': self.validated_data.get('gender', ''),
            }
        
        data.update(extra_data)
        return data

    def save(self, request):
        user = super(PatientSignUpSerializer, self).save(request)
        user.get_cleaned_data()
        user.role = 'Patient'
        user.save()
        patient = Patient(user=user)
        patient.save()
        return user

class DoctorRegisterationSerializer(RegisterSerializer):
    first_name = serializers.CharField( write_only=True, required=True, max_length = 50)
    last_name = serializers.CharField( write_only=True,max_length = 50)
    country = CountryField(write_only=True,)
    gender = serializers.ChoiceField(write_only=True,choices=GENDER)
    Phone_number = serializers.CharField(write_only=True,required = True)
    specialist = serializers.CharField(write_only=True,required=True)
    certificate = serializers.ImageField(write_only=True,required=True)
    hospital_or_center = serializers.PrimaryKeyRelatedField(write_only=True,queryset =  Hospital.objects.all())
    cv = serializers.FileField(write_only=True,required=True)


    def get_serializer_data(self):
        data = super(DoctorRegisterationSerializer, self).get_cleaned_data()
        extra_data = {  
                'first_name' : self.validated_data.get('first_name', ''),
                'last_name' : self.validated_data.get('last_name', ''),
                'Phone_number' : self.validated_data.get('Phone_number'),
                'country' : self.validated_data.get('country'),
                'gender': self.validated_data.get('gender'),
        }
        data = super(DoctorRegisterationSerializer, self).get_cleaned_data()
        data.update(extra_data)
        print(extra_data)
        print(data)
        return Response(data)


        


    def save(self, request):
        user = super(DoctorRegisterationSerializer, self).save(request)
        user.is_doctor = True
        user.role = 'doctor'
        user.save()
        doctor = Doctor(user = user ,
                        hospital = self.validated_data.get('hospital_or_center', ''),
                        specialist = self.validated_data.get('specialist', ''),
                        certificate = self.validated_data.get('certificate', ''),  
                        cv = self.validated_data.get('cv', ''))

        doctor.save()
        return user

