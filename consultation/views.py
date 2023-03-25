
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import QuestionForm ,CreateQuestionForm
# Create your views here.
def quiz(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            print("yes Valid")
            answers = form.answers_dict()
            print(answers)
            # do something with the user's answers
    else:
        form = QuestionForm()
    return render(request, 'consultation/questions.html', {'form': form})


def create_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('consultation:questions')) # replace with your desired URL
    else:
        form = CreateQuestionForm()
    return render(request, 'consultation/create_question.html', {'form': form})