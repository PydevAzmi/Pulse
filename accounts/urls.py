from django.urls import path ,include
from . import views ,api
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_views 
from rest_framework_jwt.views import obtain_jwt_token ,refresh_jwt_token

app_name = "accounts"
 
router = DefaultRouter()
router.register(r"dr-profile", api.DoctorProfileViewSet, basename="doctor_user_profile")
router.register(r"patient-profile", api.PatientProfileViewSet, basename="pateint_user_profile")
router.register(r"select-doctor", api.DoctorListViewSet,basename="select_doctor")

urlpatterns = [
    #View
    path("home/" , views.home, name = "HomePage"),
    path("register/", views.choose_register , name = "Register"),
    path("patient_register/", views.patient_register, name="PatientRegister" ),
    path("doctor_register/", views.doctor_register, name="DoctorRegister" ),
    path("login/", views.login, name="Login" ),
    path("logout/", views.logout, name="Logout"),
    #Api
    path("api/patient-register/",api.PatientRegisterApi.as_view() ,name = "patient_register"),
    path("api/doctor-register/",api.DoctorRegisterationApi.as_view() ,name = "doctor_register"),
    path("api/patient-survey/<int:pk>",api.PatientSurveyList.as_view() ,name = "patient_survey"),
    path("api/", include(router.urls)),
   #path("api/login/",api.ObtainJWTLoginViewApi.as_view() ,name = "login"),
    path("api/login/",api.LoginViewApi.as_view() ,name = "login"),
    path("api/logout/",api.LogoutView.as_view() ,name = "logout"),
    path('api/token/', rest_views.obtain_auth_token),
    path('api/token/refresh/',refresh_jwt_token,name ='token_refresh'),



]


