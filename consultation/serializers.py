from rest_framework import serializers
from .models import Survey, Review
from accounts.models import Patient


class SurveyWriteSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Survey
        exclude = ['created_at','completed', 'date_of_birth']

class SurveyReadSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source="patient.username", read_only=True)
    class Meta:
        model = Survey
        fields = '__all__'


class ReviewWriteSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Review
        exclude = ['created_at']


class ReviewReadSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source="patient.id", read_only=True)
    class Meta:
        model = Review
        exclude =  '__all__'