from django.db import models
from django.core.validators import MaxValueValidator as maxx_length, MinValueValidator as minn_length
from django.utils.translation import gettext as _
from django.utils import timezone
import datetime
# Create your models here.

Q_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('dont_know', 'Don\'t Know'),
    )
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
    patient = models.ForeignKey('accounts.User', verbose_name=_("Patient"), on_delete=models.CASCADE)
    doctor = models.ForeignKey('accounts.Doctor', related_name="doctor_reviews", verbose_name=_("Doctor"),null=True, blank=True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey('accounts.Hospital', related_name="hospital_reviews", verbose_name=_("Hospital"),null=True, blank=True, on_delete=models.SET_NULL)
    rate = models.IntegerField(_("Rate"), validators=[maxx_length(5), minn_length(0)])
    review = models.TextField(_("Review"), max_length=500)
    created_at =models.DateTimeField(_("created at"), default=timezone.now )

    def __str__(self):
        return f'{self.patient} rated {self.doctor}'
    
class Survey(models.Model):
    name = models.CharField(_("Patient Name"),null=True, blank=True, max_length=50)
    age = models.IntegerField(_("Age"),validators=[maxx_length(100), minn_length(1)], null=True, blank=True)
    date_of_birth = models.DateField(default=None, null=True ,blank=True)
    gender = models.CharField(_("Gender"), null=True, blank=True,max_length=50, choices=GENDER)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True ,blank=True)
    #questions = models.ManyToManyField("Question",related_name="survey_questions" ,verbose_name=_("Questions"))
    #answers = models.ManyToManyField("Answer", related_name=_("survey_answers"),verbose_name=_("Answers"))
    mri =models.ImageField(_("MRI"), upload_to=patient_dir_path) 
    ct = models.ImageField(_("CT"), upload_to=patient_dir_path)
    ecg = models.ImageField(_("ECG"), upload_to=patient_dir_path)
    title = models.CharField(_("Tiltle"),max_length=200)
    description = models.TextField(_("Description"),null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    completed = models.BooleanField(_("Completed"),default=False)


    ## Questions 
    question_1 = models.CharField(_("1"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_2 = models.CharField(_("2"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_3 = models.CharField(_("3"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_4 = models.CharField(_("4"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_5 = models.CharField(_("5"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_6 = models.CharField(_("6"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_7 = models.CharField(_("7"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_8 = models.CharField(_("8"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_9 = models.CharField(_("9"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_10= models.CharField(_("10"),null=True, blank=True, max_length=50, choices=Q_CHOICES)
    question_11= models.CharField(_("11"),null=True, blank=True, max_length=50, choices=Q_CHOICES)

   
    def __str__(self):
        return f'{self.patient} --> {self.name}'
    

class Question(models.Model):
    question_text = models.TextField(_("Question"))
    category = models.CharField(_("Questions Category"), max_length=50, null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Survey"),related_name="survey_ans",on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True,blank=True)
    answer_choice = models.CharField(max_length=20, choices=Q_CHOICES)

    def __str__(self) -> str:
        return str(self.survey)


class DoctorConsultationRequest(models.Model):
    doctors = models.ManyToManyField('accounts.Doctor',related_name="doctors_survey_request", blank=True)
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    status = models.CharField(_("Status"), max_length=50, choices=Q_CHOICES, default="pending")
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
    
class Report(models.Model):
    doctor = models.ForeignKey("accounts.User",related_name="doctor_report", on_delete=models.SET_NULL, null=True, blank=True)
   #patient = models.ForeignKey("accounts.User", verbose_name=_("Patient"), on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name=("survey"), on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=50)
    report_content = models.TextField()
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    
    def __str__(self):
        return f'{self.doctor}'

class MLModel(models.Model):
    survey = models.ForeignKey(Survey, related_name=("ml_survey"), on_delete=models.CASCADE)
    ecg_diagnosis = models.CharField(max_length=50)
    mri_diagnosis = models.CharField(max_length=50)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.survey}> {self.mri_diagnosis}, {self.ecg_diagnosis}'