from django import forms
from .models import Question, Choice, Comment
from django.utils.translation import gettext_lazy as _

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment_text']
		labels = {
            'comment_text': _('Comment'),
        }