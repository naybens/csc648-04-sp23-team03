from django import forms
from .models import Preference, Category, Choice

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = []

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_picked']
