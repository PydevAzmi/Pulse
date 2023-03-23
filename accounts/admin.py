from django.contrib import admin
from .models import User, Doctor, Patient, Hospital, Review

from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'Phone_number', 'country', 'password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email',)
    #list_filter = ('is_doctor',)
    
    fieldsets = (
        (None, {'fields': ('username',  'password')}),
        ('Personal info', {'fields': 
                           ('first_name', 'last_name','email',)
                           }),
        ('Permission', {
            'fields': (
                ('is_superuser','is_staff',),
                'groups'
            )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ReviewTabular(admin.TabularInline):
    model = Review

class DoctorReviews(admin.ModelAdmin):
    inlines= [ReviewTabular]
   # list_display = ["patient",'review','rate']

class HospitalReviews(admin.ModelAdmin):
    inlines= [ReviewTabular]


'''
To Add Hospital Admin With Hashing Password
admin.site.register(User, UserAdmin)
You Must Comment The Next Line '''

admin.site.register(User)
admin.site.register(Doctor, DoctorReviews)
admin.site.register(Patient)
admin.site.register(Hospital,HospitalReviews)
admin.site.register(Review)
