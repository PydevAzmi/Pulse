from django.urls import include, path 
from rest_framework.routers import DefaultRouter
from . import views, api

app_name = "consultation"

router = DefaultRouter()
router.register(r"survey", api.SurveyViewSet, basename="survey")
router.register(r"requests", api.ConsultationRequestViewSet, basename="survey_requests")
router.register(r'survey/(?P<survey_id>\d+)/reports', api.ReportViewSet, basename="survey_report")
router.register(r'survey/(?P<survey_id>\d+)/requests', api.ConsultationRequestViewSet, basename="survey_doc")
router.register(r'survey/(?P<survey_id>\d+)/reports/(?P<report_id>\d+)/review', api.ReviewViewSet, basename="report_review")
router.register(r'survey/(?P<survey_id>\d+)/intial-diagnosis', api.MLModelViewSet, basename="survey_diagnosis")


urlpatterns = [
    path("", views.survey, name='questions'),
    path("create/", views.create_question, name='create_questions'),

    path('patient/survey/', views.survey_create, name='patient_survey'),
    path('patient/survey/<int:survey_id>', views.answer_create, name='answer_create'),

    #API
    path("api/", include(router.urls)),
    path('api/doctors/', api.DoctorListView.as_view(), name='doctor-list'),
]
