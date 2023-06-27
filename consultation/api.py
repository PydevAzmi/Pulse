import os
from . import serializers
from rest_framework import permissions, viewsets, generics ,status
from .models import Survey,Review,Report,MLModel, Consultation
from accounts.models import Doctor, Patient, Hospital
from .permissions import IsPatientOrReadOnly ,IsDoctorOrReadOnly, IsPatientOrDoctorOrHospital
from rest_framework.exceptions import ValidationError
# For ML
import cv2
from PIL import Image
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
    ECG = ''
    #ECG = load_model('F:\Githup Repos\Pulse\model.h5')

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
        user = self.request.user
        patient = Patient.objects.get(user = user)
        serializer.save(patient=patient)

        # Retrieve survey data and image from request
        survey_data = serializer.validated_data
        ecg_image = survey_data.pop('ecg')
        mri_image = survey_data.pop('mri')
        ecg_image = Image.open(ecg_image)
        mri_image = Image.open(mri_image)

        # Load machine learning models
        self.ECG = load_model('F:\Githup Repos\Pulse\model.h5')
        mrimodel = load_model('MRI_MODEL.h5')

        # Define class labels
        mri_labels = {1: "normal", 0: "abnormal"}

        # Preprocess the image
        mri_image = mri_image.convert("RGB")
        mri_image = mri_image.resize((224, 224))
        mri_image = np.array(mri_image) / 255.0
        mri_image = np.expand_dims(mri_image, axis=0)
        
        def preprocess_data(image):
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (240, 200))
            img = img / 255.0
            img = np.expand_dims(img, axis=-1)
            return img

        # Make a prediction
        def predict_image(model, image):
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            preprocessed_image = preprocess_data(image)
            predictions = model.predict(np.array([preprocessed_image]))
            class_labels = ['Normal', 'Myocardial Infarction', 'History of MI', 'Abnormal Heartbeat']
            predicted_label = class_labels[np.argmax(predictions)]
            return predicted_label
        

        # predict the image class
        mri_prediction = mrimodel.predict(mri_image).argmax(axis = 1)
        mri_prediction = mri_labels[mri_prediction[0]]

        predicted_image = predict_image(self.ECG,ecg_image)

        # Create new instance of MLModelResult and save to database
        result = MLModel(   survey=serializer.instance,
                            mri_diagnosis = mri_prediction,
                            ecg_diagnosis = predicted_image)
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
        elif user.is_authenticated and user.is_hospital:
            hospital = Hospital.objects.get(user= user)
            return Consultation.objects.filter(hospital = hospital ).select_related("survey")
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
            elif user.is_authenticated and user.is_hospital:
                return serializers.ConsultationHospitalSerializer
        else:
            return serializers.ConsultationPatientSerializer

    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated, IsPatientOrReadOnly )
        elif self.action in ( "partial_update","update",):
            self.permission_classes = (IsPatientOrDoctorOrHospital, )
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
        elif user.is_authenticated and ( user.is_doctor or user.is_hospital ):
            consutation = Consultation.objects.get(id = self.kwargs["pk"])
            serializer.save( onsutation = consutation)
            return 
        