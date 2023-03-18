from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import User, Patient, Doctor 
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm

class PatientSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields= ['first_name', 'username', 'email', 'Phone_number', 'country', 'password1', 'password2']
        widgets = {
            'country': CountrySelectWidget()
        }


    @transaction.atomic
    def save(self):
        user =  super().save(commit = False)
        user.is_patient = True
        user.role = 'Patient'
        user.save()
        patient = Patient.objects.create(user = user)
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    hospital  = forms.CharField(required=True)
    certificate = forms.ImageField(required=True)
    specialist = forms.CharField(required=True)
    cv = forms.FileField(required=True)

    class Meta:
        model = User
        fields= ['first_name', 'username', 'email', 'Phone_number', 'country', 'password1', 'password2']
        widgets = {
            'country': CountrySelectWidget()
        }

    @transaction.atomic
    def save(self):
        user =  super().save(commit = False)
        user.role = 'Doctor'
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user = user)
        doctor.hospital = self.cleaned_data.get('hospital')
        doctor.cv = self.cleaned_data.get('cv')
        doctor.specialist = self.cleaned_data.get('specialist')
        doctor.certificate = self.cleaned_data.get('certificate')
        doctor.save()
        return user
    

