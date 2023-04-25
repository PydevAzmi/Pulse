from django.contrib import admin
from .models import (Review, Survey, Answer, Report, MLModel,
                     HospitalConsultationRequest, DoctorConsultationRequest,
                     Question, Answer)
# Register your models here.

class QuetionInline(admin.TabularInline):
    model = Question

class AnswerInline(admin.TabularInline):
    model = Answer
    list_display = ("tiltle" , 'answer_choice')

class QuesAswers(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
class MLInline(admin.TabularInline):
    model = MLModel

class ReportsInline(admin.TabularInline):
    model = Report

class SurveyReportMLInlines(admin.ModelAdmin):
    inlines = [
        ReportsInline,
        MLInline,
    ]

admin.site.register(Review)
admin.site.register(MLModel)
admin.site.register(Report)
admin.site.register(Question,QuesAswers)
admin.site.register(Survey,SurveyReportMLInlines)
admin.site.register(Answer)
admin.site.register(HospitalConsultationRequest)
admin.site.register(DoctorConsultationRequest)