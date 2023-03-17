from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from  django.contrib.auth.models import AbstractUser
# Create your models here.  

ROLES = (
        ('Doctor', 'doctor'),
        ('Patient', 'patient')
    )

def cv_upload(instance,filename):
    return "doctors/%s/cv/%s"%(instance.id,filename)

def certificate_upload(instance,filename):
    return "doctors/%s/certificates/%s"%(instance.id,filename)


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    role = models.CharField(_("Role"), max_length=50, choices=ROLES)
    Phone_number = models.CharField(_("Phone Number"), max_length =20)
    country = CountryField(blank= True)


class Patient(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Patient"),primary_key= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class Doctor(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Doctor"),primary_key= True, on_delete=models.CASCADE)
    hospital = models.CharField(_("Hospital"), max_length=50)
    specialist = models.CharField(_("Specialist"), max_length=50)
    cv = models.FileField(_("CV"), upload_to=cv_upload, max_length=100)

    def __str__(self):
        return self.user


class DoctorCertificates(models.Model):
    doctor = models.ForeignKey( Doctor, related_name='doctor_certificate', on_delete=models.CASCADE, verbose_name=_("Doctor"))
    certificate = models.ImageField(_("Certificate"), upload_to=certificate_upload)