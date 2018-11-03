from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from .models import Story, UserWithProfile
from django.contrib.auth.models import User


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            'title', 'message', 'category', 'author',
        ]
        labels = {
            'title': 'Título',
            'message': 'Descripción',
            'category': 'Categoría'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control noMarginAuto font32'}),
            'message': forms.Textarea(attrs={'class': 'storyMessageInput'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    username = forms.CharField(label='Nombre de usuario')
    email = forms.CharField(widget=forms.EmailInput, label='Email')

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password'
        ]
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        username = self.visible_fields()[0]
        email = self.visible_fields()[1]
        password = self.visible_fields()[2]
        username.field.widget.attrs['class'] = 'form-control createUserInput usernameInput'
        email.field.widget.attrs['class'] = 'form-control createUserInput emailInput'
        password.field.widget.attrs['class'] = 'form-control createUserInput passwordInput'


class UserProfileForm(forms.ModelForm):
    birthdate = DateField(widget=AdminDateWidget,
                          label='Fecha de nacimiento(Recuerda que si eres menor a 60 años no podrás escribir historias)')
    biography = forms.CharField(widget=forms.Textarea, label='biografía(pequeña descripción sobre tu persona)',
                                required=False)

    class Meta:
        model = UserWithProfile
        fields = [
            'birthdate', 'biography'
        ]

        labels = {
            'birthdate': 'Fecha de nacimiento',
            'biografía': 'Biografía(pequeña descripción sobre tu persona)'
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        date = self.visible_fields()[0]
        bio = self.visible_fields()[1]
        date.field.widget.attrs['class'] = 'form-control createUserInput dateInput'
        bio.field.widget.attrs['class'] = 'form-control createUserInput bioInput'

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    username = forms.CharField(label='Nombre de usuario')
    class Meta:
        model = UserWithProfile
        fields = [
            'username', 'password'
        ]