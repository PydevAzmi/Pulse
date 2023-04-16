from django.contrib import admin
from .models import Review, Question,Survey,Answer,HospitalConsultationRequest,DoctorConsultationRequest ,Report
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



admin.site.register(Review)
admin.site.register(Report)
admin.site.register(Question,QuesAswers)
admin.site.register(Survey)
admin.site.register(Answer)
admin.site.register(HospitalConsultationRequest)
admin.site.register(DoctorConsultationRequest)