from rest_framework import permissions
from accounts.models import Patient, Doctor
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


class IsPatientOrDoctor(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_patient or request.user.is_doctor)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_patient:
            patient = Patient.objects.get(user = request.user  )
            return obj.patient == patient
        elif request.user.is_authenticated and request.user.is_doctor:
            doctor = Doctor.objects.get(user = request.user)
            return doctor in obj.doctors.all()
        