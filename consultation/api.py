from .serializers import SurveyWriteSerializer ,SurveyReadSerializer
from rest_framework import permissions, viewsets
from .models import Survey
from .permissions import IsPatientOrReadOnly


class SurveyViewSet(viewsets.ModelViewSet):
    """
    CRUD Survey
    """
    

    queryset = Survey.objects.all()

    # In order to use different serializers for different 
    # actions, you can override the 
    # get_serializer_class(self) method

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return SurveyWriteSerializer

        return SurveyReadSerializer

    # get_permissions(self) method helps you separate 
    # permissions for different actions inside the same view.
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated , IsPatientOrReadOnly)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsPatientOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
