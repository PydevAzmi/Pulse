from django.urls import path 
from . import views
app_name = "consultation"
urlpatterns = [
    path("", views.survey, name='questions'),
    path("create/", views.create_question, name='create_questions'),

    path('patient/survey/', views.survey_create, name='patient_survey'),
    path('patient/survey/<int:survey_id>', views.answer_create, name='answer_create'),


    
]

'''
    path('patient/survey/', views.patient_survey, name='patient_survey'),
    path('doctor/surveys/', views.doctor_surveys, name='doctor_surveys'),
    path('doctor/survey/<int:survey_id>/', views.doctor_survey_detail, name='doctor_survey_detail'),
    path('doctor/survey/<int:survey_id>/review/', views.doctor_review_form, name='doctor_review_form'),
    path('hospital/surveys/', views.hospital_surveys, name='hospital_surveys'),
    path('hospital/survey/<int:survey_id>/', views.hospital_survey_detail, name='hospital_survey_detail'),
    path('patient/consultation/request/', views.patient_consultation_request, name='patient_consultation_request'),
    path('doctor/consultation/requests/', views.doctor_consultation_requests, name='doctor_consultation_requests'),
    path('doctor/consultation/request/<int:request_id>/', views.doctor_consultation_request_detail, name='doctor_consultation_request_detail'),
    path('doctor/consultation/request/<int:request_id>/accept/', views.doctor_consultation_request_accept, name='doctor_consultation_request_accept'),
    path('hospital/consultation/requests/', views.hospital_consultation_requests, name='hospital_consultation_requests'),
    path('hospital/consultation/request/<int:request_id>/', views.hospital_consultation_request_detail, name='hospital_consultation_request_detail'),
    '''