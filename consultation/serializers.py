from rest_framework import serializers
from .models import Survey


class SurveyWriteSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyReadSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source="patient.username", read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'