from django import forms
from .models import Exam, Marks

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        
class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = '__all__'