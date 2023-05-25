from django.shortcuts import get_object_or_404 
from requests import Response
from . import serializers
from rest_framework import permissions, viewsets, generics ,status
from .models import Survey,Review,Report,MLModel, Consultation
from accounts.models import Doctor, Patient, Hospital
from .permissions import IsPatientOrReadOnly ,IsDoctorOrReadOnly, IsPatientOrDoctor
from rest_framework.exceptions import ValidationError
# For ML
from keras.models import load_model
import numpy as np
import tensorflow as tf

class SurveyViewSet(viewsets.ModelViewSet):
    """
    CRUD Survey
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveyReadSerializer

    # for only the user who loged in
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_patient:
            patient = Patient.objects.get(user = user)
            return Survey.objects.filter(patient=patient)
        elif user.is_authenticated and user.is_doctor:
            doctor = Doctor.objects.get(user = user)
            doctor_request = Consultation.objects.get(doctors=doctor)
            if doctor_request.status == "accepted" :
                survey = doctor_request.survey.id
                return Survey.objects.filter(id=survey)
            else:
                return Survey.objects.none() 
        else:
            return Survey.objects.none() 

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.SurveyWriteSerializer
        return serializers.SurveyReadSerializer
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated, IsPatientOrReadOnly )
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsPatientOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
    
    def perform_create(self, serializer):
        patient = Patient.objects.get(user = self.request.user)
        serializer.save(patient=patient)

        # Load machine learning models
        ecgmodel = load_model('ECG_MODEL.h5')
        mrimodel = load_model('MRI_MODEL.h5')

        # Define class labels
        ecg_labels = {0: "normal", 1: "abnormal"}
        mri_labels = {1: "normal", 0: "abnormal"}

        # Retrieve survey data and image from request
        survey_data = serializer.validated_data
        ecg_image = survey_data.pop('ecg')
        mri_image = survey_data.pop('mri')
        
        from PIL import Image

        # Load the image you want to classify
        # resize to (224, 224) and normalize pixel values
        # Preprocess the image as required by the model

        mri_image = Image.open(mri_image)
        mri_image = mri_image.convert("RGB")
        mri_image = mri_image.resize((224, 224))
        mri_image = np.array(mri_image) / 255.0
        mri_image = np.expand_dims(mri_image, axis=0)


        ecg_image = Image.open(ecg_image)
        ecg_image = ecg_image.convert("RGB")
        ecg_image = ecg_image.resize((224, 224))
        ecg_image = np.array(ecg_image) / 255.0
        ecg_image = np.expand_dims(ecg_image, axis=0)


        # predict the image class
        mri_prediction = mrimodel.predict(mri_image).argmax(axis = 1)
        mri_prediction = mri_labels[mri_prediction[0]]

        ecg_prediction = ecgmodel.predict(ecg_image).argmax(axis = 1)
        ecg_prediction = ecg_labels[ecg_prediction[0]]

        # Create new instance of MLModelResult and save to database
        result = MLModel(   survey=serializer.instance,
                            mri_diagnosis = mri_prediction,
                            ecg_diagnosis = ecg_prediction)
        result.save()
        

    def perform_update(self, serializer):
        patient = Patient.objects.get(user = self.request.user)
        serializer.save(patient=patient)

class ReviewViewSet(viewsets.ModelViewSet):
    """
    CRUD Review
    """
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_patient:
            patient = Patient.objects.get(user = user)
            return Review.objects.filter(patient=patient)      
        elif user.is_authenticated and user.is_doctor:
            doctor = Doctor.objects.get(user = user)
            return Review.objects.filter(doctor=doctor)
        else :
            return Review.objects.none()

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
    
    def perform_create(self, serializer):
        report_id = self.kwargs['report_id']
        report = Report.objects.get(id=report_id)
        patient = Patient.objects.get(user = self.request.user)
        
        existing_review = Review.objects.filter(patient=patient, doctor = report.doctor).exists()
        if existing_review:
            raise ValidationError('You can only create one Review for a single Report.')
        else:
            serializer.save(patient=patient, doctor = report.doctor )

    def perform_update(self, serializer):
        report_id = self.kwargs['report_id']
        report = Report.objects.get(id=report_id)
        serializer.save(patient=self.request.user, doctor = report.doctor )

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
        doctor = Doctor.objects.get(user = self.request.user)
        survey = Survey.objects.get(id=survey_id)
        existing_report = Report.objects.filter(doctor=doctor, survey = survey).exists()
        if existing_report:
            raise ValidationError('You can only create one report for a single survey.')
        else:
            serializer.save(doctor=doctor, survey = survey)

    def perform_update(self, serializer):
        survey_id = self.kwargs['survey_id']
        doctor = Doctor.objects.get(user = self.request.user)
        survey = Survey.objects.get(id=survey_id)
        serializer.save(doctor=doctor, survey = survey)
        
class MLModelViewSet(viewsets.ModelViewSet):
    """
    ML models result
    """

    def get_queryset(self):
        survey_id = self.kwargs['survey_id']
        queryset = MLModel.objects.filter(survey=survey_id)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return serializers.MLmodelWriteSerializer
        return serializers.MLmodelReadSerializer
    
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

class DoctorListView(generics.ListAPIView):
    serializer_class = serializers.DoctorSerializer
    permission_classes = (permissions.IsAuthenticated, IsPatientOrReadOnly)

    def get_queryset(self):
        queryset = Doctor.objects.all().select_related("hospital")
        specialist = self.request.query_params.get('specialist', None)
        if specialist is not None:
            queryset = queryset.filter(specialist__icontains=specialist)
        return queryset

class HospitalsListView(generics.ListAPIView):
    serializer_class = serializers.HospitalSerializer
    permission_classes = (permissions.IsAuthenticated, IsPatientOrReadOnly)
    queryset = Hospital.objects.all()

class ConsultationRequestViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsPatientOrReadOnly)

    # for only the user who loged in
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_patient:
            patient = Patient.objects.get(user = user)
            return Consultation.objects.filter(patient=patient)
        elif user.is_authenticated and user.is_doctor:
            doctor = Doctor.objects.get(user = user)
            return Consultation.objects.filter(doctors=doctor).select_related("survey")
        else:
            return Consultation.objects.none() 
        
    def get_serializer_class(self):
        user = self.request.user
        if self.action in ("create", "destroy" ):
            return serializers.ConsultationPatientSerializer
        elif self.action in ('update',"partial_update",'retrieve' ):
            if user.is_authenticated and user.is_patient:
                return serializers.ConsultationPatientSerializer
            elif user.is_authenticated and user.is_doctor:
                return serializers.ConsultationDoctorSerializer
        else:
            return serializers.ConsultationPatientSerializer

    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated, IsPatientOrReadOnly )
        elif self.action in ( "partial_update","update",):
            self.permission_classes = (IsPatientOrDoctor, )
        elif self.action in ( "destroy",):
            self.permission_classes = (IsPatientOrReadOnly, )
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
    
    def perform_create(self, serializer):
        # Check if consultation request already exists for the patient
        patient = Patient.objects.get(user = self.request.user)
        survey_id = self.kwargs['survey_id']
        survey = Survey.objects.get(id = survey_id)
        existing_consultation_request = Consultation.objects.filter(patient=patient, survey = survey).exists()
        if existing_consultation_request:
            raise ValidationError('You can only create one consultation request for a single survey.')
        else:
            serializer.save(patient=patient, survey = survey, )

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_authenticated and user.is_patient:
            survey_id = self.kwargs['survey_id']
            survey = Survey.objects.get(id = survey_id)
            serializer.save(patient=survey.patient, survey = survey, )
            return
        elif user.is_authenticated and user.is_doctor:
            consutation = Consultation.objects.get(id = self.kwargs["pk"])
            serializer.save( onsutation = consutation)
            return 

        