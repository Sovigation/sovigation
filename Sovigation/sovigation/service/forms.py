from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['user', 'grade', 'credit', 'semester', 'major', 'subject']
