from django.urls import path ,re_path
from . import views
from . import api
from rest_auth.registration.views import VerifyEmailView
app_name = "accounts"
urlpatterns = [
    #View
    path("home/" , views.home, name = "HomePage"),
    path("register/", views.choose_register , name = "Register"),
    path("patient_register/", views.patient_register, name="PatientRegister" ),
    path("doctor_register/", views.doctor_register, name="DoctorRegister" ),
    path("login/", views.login, name="Login" ),
    path("logout/", views.logout, name="Logout" ),
    
    
    #Api
    path("api/patient-register/",api.PatientRegisterApi.as_view() ,name = "patient_register"),
    path("api/doctor-register/",api.DoctorRegisterationApi.as_view() ,name = "doctor_register"),
    path("api/login/",api.ObtainJWTLoginViewApi.as_view() ,name = "login"),
    path("api/logout/",api.User_logout ,name = "logout"),



]


