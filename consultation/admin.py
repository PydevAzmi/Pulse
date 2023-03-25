from django.contrib import admin
from .models import Review, Question,Survey
# Register your models here.
admin.site.register(Review)
admin.site.register(Question)
admin.site.register(Survey)