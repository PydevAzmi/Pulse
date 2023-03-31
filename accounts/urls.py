from django.urls import path 
from . import views
from . import api
app_name = "accounts"
urlpatterns = [
    path("home/" , views.home, name = "HomePage"),
    path("register/", views.choose_register , name = "Register"),
    path("patient_register/", views.patient_register, name="PatientRegister" ),
    path("doctor_register/", views.doctor_register, name="DoctorRegister" ),
    path("login/", views.login, name="Login" ),
    path("logout/", views.logout, name="Logout" ),
    
    
    
    path("api/patient-register/",api.PatientRegisterApi.as_view() ,name = "patient_register"),
    path("api/doctor-register/",api.DoctorRegisterationApi.as_view() ,name = "doctor_register"),

]


