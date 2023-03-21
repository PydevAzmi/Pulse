from django.contrib import admin
from .models import User, Doctor, Patient, Hospital, Review
# Register your models here.

class ReviewTabular(admin.TabularInline):
    model = Review

class DoctorReviews(admin.ModelAdmin):
    inlines= [ReviewTabular]
   # list_display = ["patient",'review','rate']

admin.site.register(User)
admin.site.register(Doctor, DoctorReviews)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Review)
