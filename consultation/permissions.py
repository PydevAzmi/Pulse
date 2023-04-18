from rest_framework import permissions

class IsPatientOrReadOnly(permissions.BasePermission):
    """
    Check if Patient is author of the Survey.
    """
    def has_permission(self, request, view):
        return request.user.is_patient 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.patient == request.user 


class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Check if Doctor is author of the Report.
    """
    def has_permission(self, request, view):
        return request.user.is_doctor 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.doctor == request.user 
