from django.db import models
from django.core.validators import MaxValueValidator as maxx_length, MinValueValidator as minn_length
from django.utils.translation import gettext as _
from django.utils import timezone
# Create your models here.

GENDER = [ 
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

CHOICES = [
    ("pending","pending"),
    ("accepted", "accepted"),
    ("rejected","rejeted"),
]


def patient_dir_path(instance, filename):
    return 'patients/{0}/{1}/Scans/{2}'.format(instance.patient, instance.name, filename)

class Review(models.Model):
    patient = models.ForeignKey('accounts.Patient', verbose_name=_("Patient"), on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.Doctor', related_name="doctor_reviews", verbose_name=_("Doctor"),null=True, blank=True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey('accounts.Hospital', related_name="hospital_reviews", verbose_name=_("Hospital"),null=True, blank=True, on_delete=models.SET_NULL)
    rate = models.IntegerField(_("Rate"), validators=[maxx_length(5), minn_length(0)])
    review = models.TextField(_("Review"), max_length=500)
    created_at =models.DateTimeField(_("created at"), default=timezone.now )

    def __str__(self):
        return f'{self.patient.user.username} rated {self.doctor.user.username}'
    
class Survey(models.Model):
    name = models.CharField(_("Patient Name"),null=True, blank=True, max_length=50)
    age = models.IntegerField(_("Age"),validators=[maxx_length(100), minn_length(1)], null=True, blank=True)
    date_of_birth = models.DateField(default=None, null=True ,blank=True)
    gender = models.CharField(_("Gender"), null=True, blank=True,max_length=50, choices=GENDER)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    #questions = models.ManyToManyField("Question",related_name="survey_questions" ,verbose_name=_("Questions"))
    #answers = models.ManyToManyField("Answer", related_name=_("survey_answers"),verbose_name=_("Answers"))
    mri =models.FileField(_("MRI"), upload_to=patient_dir_path) 
    ct = models.FileField(_("CT"), upload_to=patient_dir_path)
    ecg = models.FileField(_("ECG"), upload_to=patient_dir_path)
    title = models.CharField(_("Tiltle"),max_length=200)
    description = models.TextField(_("Description"),null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    completed = models.BooleanField(_("Completed"),default=False)
    
    def __str__(self):
        return f'{self.patient} --> {self.name}'
    

class Question(models.Model):
    question_text = models.TextField(_("Question"))
    category = models.CharField(_("Questions Category"), max_length=50, null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    survey = models.ManyToManyField(Survey, verbose_name=_("Survey"),related_name="survey_ans")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('dont_know', 'Don\'t Know'),
    )
    answer_choice = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self) -> str:
        return str(self.survey)


class DoctorConsultationRequest(models.Model):
    doctors = models.ManyToManyField('accounts.Doctor',related_name="doctors_survey_request", blank=True)
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    status = models.CharField(_("Status"), max_length=50, choices=CHOICES, default="pending")
    accepted_doctor = models.ForeignKey(
        'accounts.Doctor',
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='accepted_D_consultation_requests'
    )

    def __str__(self):
        return f'{self.survey.patient} - {self.created_at}'
    
class HospitalConsultationRequest(models.Model):
    doctors = models.ManyToManyField('accounts.Hospital',related_name="Hospital_survey_request", blank=True)
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    status = models.CharField(_("Status"), max_length=50, choices=CHOICES, default="pending")

    accepted_hospitals = models.ForeignKey(
        'accounts.Doctor',
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='accepted_H_consultation_requests'
    )

    def __str__(self):
        return f'{self.survey.patient} - {self.created_at}'