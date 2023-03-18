from django.contrib import admin
from .models import User, Doctor, Patient
# Register your models here.

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)