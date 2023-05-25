from rest_framework import permissions
from accounts.models import Patient, Doctor, Hospital
from consultation.models import Consultation
class IsPatientOrReadOnly(permissions.BasePermission):
    """
    Check if Patient is author of the Survey.
    """
    def has_permission(self, request, view):
        return request.user.is_patient 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        patient = Patient.objects.get(user = request.user  )
        return obj.patient == patient


class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Check if Doctor is author of the Report.
    """
    def has_permission(self, request, view):
        return request.user.is_doctor 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        doctor = Doctor.objects.get(user = request.user)
        return obj.doctor == doctor 


class IsPatientOrDoctorOrHospital(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_patient or user.is_doctor or user.is_hospital)
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_authenticated and user.is_patient:
            patient = Patient.objects.get(user = user  )
            return obj.patient == patient
        elif user.is_authenticated and user.is_doctor:
            doctor = Doctor.objects.get(user = user)
            return doctor in obj.doctors.all()
        elif user.is_authenticated and user.is_hospital:
            hospital = Hospital.objects.get(user = user)
            return hospital in obj.hospital.all()
        