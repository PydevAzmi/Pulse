from allauth.account.adapter import get_adapter
from .models import Patient, Doctor, Hospital, User
from django.contrib.auth import login
# For Registeration
from rest_auth.registration.serializers import RegisterSerializer 
from django_countries.serializer_fields  import CountryField

# for Login & Logout
from django.contrib.auth import authenticate, user_logged_in
from rest_framework import serializers 
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from consultation.serializers import ReviewReadSerializer, ReportReadSerializer

GENDER = {
    'Male': 'Male',
    'Female': 'Female'
} 

def handle_uploaded_file(file):
    with open(file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file.name

class PatientSignUpSerializer(RegisterSerializer):
    first_name = serializers.CharField( write_only=True, required=True,max_length = 50)
    last_name = serializers.CharField(max_length = 50)
    country = CountryField()
    gender = serializers.ChoiceField(choices=GENDER)
    Phone_number = serializers.CharField()
   
   
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name' : self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
            'Phone_number' : self.validated_data.get('Phone_number', ''),
            'country' : self.validated_data.get('country', ''),
            'gender': self.validated_data.get('gender', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.role = 'Patient'
        user.is_patient = True
        user.Phone_number = self.cleaned_data.get('Phone_number')
        user.country = self.cleaned_data.get('country')
        user.gender = self.cleaned_data.get('gender')
        adapter.save_user(request, user, self)
        patient = Patient(user = user)
        patient.save()
        return user
    
class HospitalAdminSignUpSerializer(RegisterSerializer):
    first_name = serializers.CharField( write_only=True, required=True,max_length = 50)
    last_name = serializers.CharField(max_length = 50)
    country = CountryField()
    gender = serializers.ChoiceField(choices=GENDER)
    Phone_number = serializers.CharField()
   
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name' : self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
            'Phone_number' : self.validated_data.get('Phone_number', ''),
            'country' : self.validated_data.get('country', ''),
            'gender': self.validated_data.get('gender', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.role = 'doctor'
        user.is_hospital = True
        user.Phone_number = self.cleaned_data.get('Phone_number')
        user.country = self.cleaned_data.get('country')
        user.gender = self.cleaned_data.get('gender')
        adapter.save_user(request, user, self)
        return user
       
class DoctorRegisterationSerializer(RegisterSerializer):

    first_name = serializers.CharField(write_only=True, required=True, max_length=50)
    last_name = serializers.CharField(write_only=True, max_length=50)
    country = CountryField()
    gender = serializers.ChoiceField(write_only=True, choices=GENDER)
    Phone_number = serializers.CharField(write_only=True, required=True)
    specialist = serializers.CharField(write_only=True, required=True)
    certificate = serializers.ImageField(write_only=True, required=True)
    hospital_or_center = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Hospital.objects.all())
    cv = serializers.FileField(write_only=True, required=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name' : self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name', ''),
            'Phone_number' : self.validated_data.get('Phone_number', ''),
            'country' : self.validated_data.get('country', ''),
            'gender': self.validated_data.get('gender', ''),
            'specialist': self.validated_data.get('specialist', ''),
            'certificate': self.validated_data.get('certificate', ''),
            'hospital_or_center': self.validated_data.get('hospital_or_center'),
            'cv': self.validated_data.get('cv'),
     }
    

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.role = 'Doctor'
        user.is_doctor = True
        user.Phone_number = self.cleaned_data.get('Phone_number')
        user.country = self.cleaned_data.get('country')
        user.gender = self.cleaned_data.get('gender')
        adapter.save_user(request, user, self)
        doctor = Doctor(
            user=user,
            hospital= self.cleaned_data['hospital_or_center'],
            specialist = self.cleaned_data['specialist'],
            certificate = (self.cleaned_data['certificate']),
            cv = (self.cleaned_data['cv'])
        )
        doctor.save()
        return user
    
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
       
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'first_name', 'last_name', 'email', 'Phone_number']
        
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id',"name"]

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only= True)
    hospital =HospitalSerializer(read_only= True)
    review = ReviewReadSerializer(read_only = True)
    class Meta:
        model = Doctor
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Patient
        fields = "__all__"

class UserUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"





'''
class LoginJWTSerializer(JSONWebTokenSerializer):

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)
                
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
 
'''
