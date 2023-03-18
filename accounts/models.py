from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from  django.contrib.auth.models import AbstractUser
# Create your models here.  

ROLES = (
        ('Doctor', 'doctor'),
        ('Patient', 'patient')
    )

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'doctors/user_{0}/{1}'.format(instance.user, filename)

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    role = models.CharField(_("Role"), max_length=50, choices=ROLES)
    Phone_number = models.CharField(_("Phone Number"), max_length =20)
    country = CountryField(blank= True)


class Patient(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Patient"), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Doctor(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Doctor"), on_delete=models.CASCADE)
    hospital = models.CharField(_("Hospital"), max_length=50)
    specialist = models.CharField(_("Specialist"), max_length=50)
    cv = models.FileField(_("CV"), upload_to = user_directory_path, max_length=100)
    certificate = models.ImageField(_("Certificate"), upload_to =user_directory_path )
    profile_photo = models.ImageField(_("Profile Photo"),upload_to =user_directory_path )

    def __str__(self):
        return str(self.user)