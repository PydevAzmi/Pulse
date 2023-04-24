from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Survey, Review  ,Report,MLModel
from accounts.models import Patient,User

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

