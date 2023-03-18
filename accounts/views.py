from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import PatientSignUpForm, DoctorSignUpForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login , logout as out

# Create your views here.
def home(request):
    return render(request, 'registration/home.html' )


def choose_register(request):
    return render(request, "registration/choose_login.html")


def patient_register(request):
    if request.method == "POST":
        patient_register_form = PatientSignUpForm(request.POST,request.FILES)
        if patient_register_form.is_valid():
            patient_register_form.save()
    else:
        patient_register_form = PatientSignUpForm()

    context ={
        "patient_register_form" : patient_register_form
    }
    
    return render(request, "registration/patient_register.html", context)


def doctor_register(request):
    if request.method == "POST":
        doctor_register_form = DoctorSignUpForm(request.POST,request.FILES)
        if doctor_register_form.is_valid():
            doctor_register_form.save()
    else:
        doctor_register_form = DoctorSignUpForm()

    context ={
        "doctor_register_form" : doctor_register_form ,
    }
    return render(request, "registration/doctor_register.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm( data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password= form.cleaned_data.get("password")
            user_login = authenticate(request, username = username, password = password)
            if user_login is not None:
                auth_login(request, user_login)
                return redirect(reverse('accounts:HomePage'))
    else:
        form = AuthenticationForm()

    context = {
        "form" : form
        }

    return render(request, "registration/login.html", context)


def logout(request):
    out(request)
    return redirect("/accounts/home")