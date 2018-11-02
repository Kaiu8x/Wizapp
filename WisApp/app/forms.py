from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            'title', 'message', 'category','author',
        ]
        labels = {
            'title': 'Título',
            'message': 'Descripción',
            'category' : 'Categoría'
        }
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control noMarginAuto'}),
            'message' : forms.Textarea(attrs={'class': 'storyMessageInput'}),
        }