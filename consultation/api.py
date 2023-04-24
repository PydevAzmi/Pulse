from django.shortcuts import get_object_or_404
from requests import Response
from . import serializers
from rest_framework import permissions, viewsets
from .models import Survey,Review,Report,MLModel
from .permissions import IsPatientOrReadOnly ,IsDoctorOrReadOnly


from keras.models import load_model
import numpy as np

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
        serializer.save(patient=self.request.user)

        # Load machine learning models
        ecgmodel = load_model('ECG_MODEL.h5')
        mrimodel = load_model('MRI_MODEL.h5')

        # Retrieve survey data and image from request
        survey_data = serializer.validated_data
        ecg_image = survey_data.pop('ecg')
        mri_image = survey_data.pop('mri')

        from PIL import Image
        # Preprocess the image as required by the model
        # resize to (224, 224) and normalize pixel values
        ecg_image = Image.open(ecg_image)
        ecg_image = ecg_image.resize((224, 224))
        ecg_image = np.array(ecg_image) / 255.0
        ecg_image = np.expand_dims(ecg_image, axis=0)

        mri_image = Image.open(mri_image)
        mri_image = mri_image.convert("RGB")
        mri_image = mri_image.resize((224, 224))
        mri_image = np.array(mri_image) 
        mri_image = np.expand_dims(mri_image, axis=0)


        # Use model to make predictions on image data
        mri_prediction = mrimodel.predict(mri_image)
        print(f"MRI : {mri_prediction}")

        ecg_prediction = ecgmodel.predict(ecg_image)
        print(f"MRI : {mri_prediction}")
        
        # Create new instance of MLModelResult and save to database
        result = MLModel(   survey=serializer.instance,
                            mri_diagnosis = str(mri_prediction),
                            ecg_diagnosis = str(ecg_prediction))
        
        result.save()
        

    def perform_update(self, serializer):
        serializer.save(patient=self.request.user)

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
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]