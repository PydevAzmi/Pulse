from django import forms
from .models import Question ,Survey, Question,Answer,GENDER ,Q_CHOICES
from django.db import transaction

    
class SurveyForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        for question in (Question.objects.filter(is_active=True)) :
            self.fields[f'Q-{question.id}'] = forms.ChoiceField(
                                choices=Q_CHOICES,
                                widget=forms.RadioSelect,
                                label=question.question_text
                                )
    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        survey = super().save(commit = False)   
        survey.title = f"patient - {self.cleaned_data.get('name')}"
        survey.save()
        
        for question in (Question.objects.filter(is_active=True)) :
            submission = Answer.objects.create(survey = survey)
            submission.question = question
            submission.answer_choice = data[f'Q-{question.id}']
            submission.save()

    class Meta:
        model = Survey
        fields = ['name',"age", 'gender','mri','ecg','description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'category']


class AnswerForm(forms.ModelForm):
    answer_choice = forms.ChoiceField(choices=Q_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Answer
        fields = ['question', 'answer_choice']


'''
class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        questions = Question.objects.filter(is_active=True)
        for question in questions:
            if question.question_type == 'MC':
                choices = question.answer_text.split('\n')
                self.fields[question.id] = forms.ChoiceField(
                                choices=[(c.strip(), c.strip()) for c in choices],
                                widget=forms.RadioSelect,
                                label=question.question_text
                                )
                
            elif question.question_type == 'TF':
                self.fields[question.id] = forms.BooleanField(
                                widget=forms.RadioSelect(choices=[('Yes', 'Yes'), ('No', 'No')]),
                                label=question.question_text)
    class Meta : 
        model = Question
        fields = ["question_text","answer_text"]
                


    def answers_dict(self):
        answers = {}
        for field in self.fields:
            answers[field] = self.cleaned_data[field]
        return answers
'''

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [ 'question_text', 'category', 'is_active']
        


