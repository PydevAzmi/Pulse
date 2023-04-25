from rest_framework import permissions
from .models import Patient, Doctor
class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Check if Doctor is Owner of the Profile.
    """
    def has_permission(self, request, view):
        return request.user.is_doctor 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        patient = Patient.objects.get(user = request.user  )
        return obj.patient == patient

class IsPatientOrReadOnly(permissions.BasePermission):
    """
    Check if Patient is author of the Survey.
    """
    def has_permission(self, request, view):
        return request.user.is_patient 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        doctor = Doctor.objects.get(user = request.user)
        return obj.doctor == doctor
