from django.urls import include, path 
from rest_framework.routers import DefaultRouter
from . import views , api

app_name = "consultation"

router = DefaultRouter()
router.register(r"survey", api.SurveyViewSet)
router.register(r"review", api.ReviewViewSet)


urlpatterns = [
    path("", views.survey, name='questions'),
    path("create/", views.create_question, name='create_questions'),

    path('patient/survey/', views.survey_create, name='patient_survey'),
    path('patient/survey/<int:survey_id>', views.answer_create, name='answer_create'),

    #API
    path("api/", include(router.urls)),
]
