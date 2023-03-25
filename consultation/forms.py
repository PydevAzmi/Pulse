from django import forms
from .models import Question


CHOICES=[
        ('Yes', 'Yes'),
        ('No', 'No'),
        ]


class SurveyForm(forms.Form):
    your_form_field_name = forms.CharField(label='What should you do?', widget=forms.Select(choices=CHOICES))


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

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'question_text', 'answer_text', 'is_active']
        widgets = {
            'question_type': forms.Select(attrs={
                                        'class': 'form-control'
                                        }),
            'question_text': forms.Textarea(attrs={
                                        'class': 'form-control'
                                        }),
            'answer_text': forms.Textarea(attrs={
                                        'class': 'form-control'
                                        }),
            'is_active': forms.CheckboxInput(attrs={
                                        'class': 'form-check-input'
                                        }),
        }


