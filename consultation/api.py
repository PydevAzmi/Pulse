from django.shortcuts import get_object_or_404
from requests import Response
from . import serializers
from rest_framework import permissions, viewsets
from .models import Survey,Review,Report
from .permissions import IsPatientOrReadOnly ,IsDoctorOrReadOnly


class SurveyViewSet(viewsets.ModelViewSet):
    """
    CRUD Survey
    """

    queryset = Survey.objects.all()
    serializer_class = serializers.SurveyReadSerializer

    # for only the user who loged in
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_patient:
            return Survey.objects.filter(patient=user)      
        else:
            return Survey.objects.none() 

        
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.SurveyWriteSerializer
        return serializers.SurveyReadSerializer
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,IsPatientOrReadOnly )
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsPatientOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    """
    CRUD Review
    """
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.ReviewWriteSerializer
        return serializers.ReviewReadSerializer 
        
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated , IsPatientOrReadOnly)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsPatientOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()

class ReportViewSet(viewsets.ModelViewSet):
    """
    CRUD Report
    """

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        queryset = Report.objects.filter(survey=survey_id)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.ReportWriteSerializer
        return serializers.ReportReadSerializer

        
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsDoctorOrReadOnly]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsDoctorOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        survey_id = self.kwargs['survey_id']
        serializer.save(doctor=self.request.user, survey = Survey.objects.get(id=survey_id))

    def perform_update(self, serializer):
        survey_id = self.kwargs['survey_id']
        serializer.save(doctor=self.request.user, survey = Survey.objects.get(id=survey_id))
        
