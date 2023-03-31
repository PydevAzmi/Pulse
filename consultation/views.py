
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Survey ,Question, Answer
from .forms import  CreateQuestionForm, SurveyForm, AnswerForm

# Create your views here.


@login_required
def survey_create(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST, request.FILES)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.patient = request.user
            survey.save()
            return redirect('consultation:answer_create', survey_id=survey.id)
    else:
        form = SurveyForm()
    return render(request, 'consultation/survey_form.html', {'form': form})

@login_required
def answer_create(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.survey = survey
            answer.save()
            print( 'Answer added successfully!')
            return redirect('consultation:answer_create', survey_id=survey.id)
    else:
        form = AnswerForm()

    context = {
        'survey': survey,
        'questions': Question.objects.filter(is_active=True),
        'form': form
    }
    return render(request, 'consultation/answer_form.html', context)



@login_required
def survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.patient = request.user
            form.save()
            return redirect(reverse(f'consultation:answer_create {form.instance.pk} '))
    else:
        form = SurveyForm()
    return render(request, 'consultation/questions.html', {'form': form})


## For Doctors To Create Their Own Questions
@login_required
def create_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('consultation:questions')) 
    else:
        form = CreateQuestionForm()
    return render(request, 'consultation/create_question.html', {'form': form})