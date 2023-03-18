from django.urls import path 
from . import views
app_name = "accounts"
urlpatterns = [
    path("home/" , views.home, name = "HomePage"),
    path("register/", views.choose_register , name = "Register"),
    path("patient_register/", views.patient_register, name="PatientRegister" ),
    path("doctor_register/", views.doctor_register, name="DoctorRegister" ),
    path("login/", views.login, name="Login" ),
    path("logout/", views.logout, name="Logout" )
]

