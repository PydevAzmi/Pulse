from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Survey, Review, Report, MLModel, Consultation, CHOICES
from accounts.models import Patient, User, Doctor,Hospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id',"admin","name","country_address", 'image']

class DoctorSerializer(serializers.ModelSerializer):
    hospital =HospitalSerializer(read_only= True)
    class Meta:
        model = Doctor
        fields = ('id', 'user', 'hospital', 'specialist', 'profile_photo', 'exp', 'fee')

class ReviewWriteSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Review
        exclude = ['created_at',]

class ReviewReadSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source="patient.id", read_only=True)
    class Meta:
        model = Review
        fields =  '__all__'

class MLmodelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        exclude = ['created_at','survey']

class MLmodelReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = '__all__'

class ReportWriteSerializer(serializers.ModelSerializer):
    doctor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Report
        exclude = ['created_at','survey']

class ReportReadSerializer(serializers.ModelSerializer):
    reviews = ReviewWriteSerializer(read_only=True)
    doctor = serializers.CharField(source="doctor.id", read_only=True)
    class Meta:
        model = Report
        fields = '__all__'
        
class SurveyWriteSerializer(serializers.ModelSerializer):
    reports = ReportReadSerializer(many = True, read_only = True)
    ml_models = MLmodelReadSerializer(many = True, read_only = True)
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Survey
        exclude = ['created_at','completed',"age", ]

class SurveyReadSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source="patient.username", read_only=True)
    class Meta:
        model = Survey
        fields = '__all__'

class SurveyRead_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class ConsultationPatientSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.ChoiceField(choices=CHOICES, read_only = True)
    class Meta:
        model = Consultation
        exclude = ['created_at','survey',]

class ConsultationDoctorSerializer(serializers.ModelSerializer):
    survey =SurveyRead_Serializer(read_only = True)
    class Meta:
        model = Consultation
        exclude = ['hospital',]


class ConsultationHospitalSerializer(serializers.ModelSerializer):
    survey =SurveyRead_Serializer(read_only = True)
    class Meta:
        model = Consultation
        exclude = ['doctors',]
