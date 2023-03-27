from django.contrib import admin
from .models import Review, Question,Survey,Answer,HospitalConsultationRequest,DoctorConsultationRequest
# Register your models here.

class QuetionInline(admin.TabularInline):
    model = Question

class AnswerInline(admin.TabularInline):
    model = Answer

class QuesAswers(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]



admin.site.register(Review)
admin.site.register(Question,QuesAswers)
admin.site.register(Survey)
admin.site.register(Answer)
admin.site.register(HospitalConsultationRequest)
admin.site.register(DoctorConsultationRequest)