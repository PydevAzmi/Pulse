from django.urls import path 
from . import views
app_name = "consultation"
urlpatterns = [
    path("", views.quiz, name='questions'),
    path("create/", views.create_question, name='create_questions'),
]