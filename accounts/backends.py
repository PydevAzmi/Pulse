from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import BaseAuthentication
from .models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_auth = JSONWebTokenAuthentication()
        result = jwt_auth.authenticate(request)
        if result is None:
            return None
        else:
            token, user, redirect_to = result
            print(result)
        return (user, token, redirect_to)
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
       