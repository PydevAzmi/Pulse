from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser ,AbstractBaseUser
from django.core.validators import MaxValueValidator as maxx_length, MinValueValidator as minn_length
# Create your models here.  


ROLES = (
        ('Doctor', 'doctor'),
        ('Patient', 'patient')
    )

H_MODEL = (
        ('Hospital' , 'hospital'),
        ('Center' , 'center'),
    )

GENDER = [ 
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/doctors/Dr_{1}/{2}'.format(instance.hospital, instance.user, filename)

def hospital_dir_path(instance, filename):
    return '{0}/{1}_images/{2}'.format(instance.name,instance.model,filename) 


def patient_dir_path(instance, filename):
    return 'patients/{0}/profile_photo/{1}'.format(instance.user, filename)


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(_("Is Hospital"), default= False)
    role = models.CharField(_("Role"), max_length=50, choices=ROLES)
    Phone_number = models.CharField(_("Phone Number"), max_length =20)
    country = CountryField(blank= True)
    gender = models.CharField(_("Gender"), max_length=50, choices=GENDER)
    

class Patient(models.Model):
    user = models.OneToOneField(User,related_name='User_Patient', verbose_name=_("Patient"), on_delete=models.CASCADE)
    profile_photo = models.ImageField(_("Profile Photo"), upload_to = patient_dir_path )
    
    def __str__(self):
        return str(self.user)
    

class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='User_Doctor', verbose_name=_("Doctor"), on_delete=models.CASCADE)
    hospital = models.ForeignKey("Hospital", related_name='Hospital_Doctors', verbose_name=_("Hospital or Center"), on_delete=models.CASCADE, blank=True, null=True)
    specialist = models.CharField(_("Specialist"), max_length=50)
    cv = models.FileField(_("CV"), upload_to = user_directory_path, max_length=100, null=True, blank=True)
    certificate = models.ImageField(_("Certificate"), upload_to =user_directory_path ,null=True, blank=True)
    profile_photo = models.ImageField(_("Profile Photo"),upload_to =user_directory_path, null=True, blank=True )
    exp = models.IntegerField(_("Doctor Experience"), null=True , blank=True)
    fee = models.DecimalField(_("Doctor Fee"),max_digits=7, decimal_places=2, default=0.00, null=True, blank=True)
    review = models.ForeignKey("Review",related_name="doctor_reviews", verbose_name=_("Review"), on_delete=models.CASCADE , null=True, blank=True)
    education = models.CharField(max_length=255, null=True , blank= True)

    def __str__(self):
        return str(self.user)
    

class Hospital(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    admin = models.OneToOneField(User, verbose_name=_("Admin"),related_name="hospital_admin" , on_delete=models.CASCADE)
    description = models.TextField(_("Description"), max_length=500)
    country_address = CountryField(blank=True)
    Address = models.CharField(_("Address"), max_length=50)
    image = models.ImageField(_("Image"), upload_to=hospital_dir_path)
    model = models.CharField(_("Model"), choices=H_MODEL, max_length=50)
    fee = models.DecimalField(_("Fee"),max_digits=7, decimal_places=2, default=0.00, null=True , blank=True)
    review = models.ForeignKey("Review",related_name="hospital_reviews", verbose_name=_("Review"), on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return str(self.name)
    

class Review(models.Model):
    patient = models.ForeignKey(Patient ,verbose_name=_("Patient"), on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor , related_name="doctor_reviews", verbose_name=_("Doctor"),null=True, blank=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital , related_name="hospital_reviews", verbose_name=_("Hospital"),null=True, blank=True, on_delete=models.CASCADE)
    rate = models.IntegerField(_("Rate"), validators=[maxx_length(5), minn_length(0)])
    review = models.TextField(_("Review"), max_length=500)
    created_at =models.DateTimeField(_("created at"), default=timezone.now )

    
    def __str__(self):
        return f'{self.patient.user.username} rated {self.doctor.user.username}'