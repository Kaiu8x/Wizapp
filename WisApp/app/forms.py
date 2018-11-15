from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import FileInput, CheckboxSelectMultiple
from django.forms.fields import DateField
from .models import Story, UserWithProfile, Comment, PetitionForAdmin
from django.contrib.auth.models import User


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        image = forms.ImageField(required=False, widget=FileInput,label='Elegir imagen')
        fields = [
            'title', 'message', 'category','image'
        ]
        labels = {
            'title': 'Título',
            'message': 'Descripción',
            'category': 'Categoría/Evento',
            'image':'imagen'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mx-auto font32'}),
            'message': forms.Textarea(attrs={'class': 'storyMessageInput keepWhitespaceFormatting'}),
        }

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['message'].strip = False

class PetitionAdmin( forms.ModelForm ):
    class Meta:
        model = PetitionForAdmin
        message = forms.CharField( widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
        fields = [
            'title', 'message',
        ]
        labels = {
            'title': 'Título',
            'message': 'Descripción',
        }
    def __init__(self, *args, **kwargs):
        super(PetitionAdmin, self).__init__(*args, **kwargs)


class PetitionForm(forms.ModelForm):
    class Meta:
        model = PetitionForAdmin
        image = forms.ImageField(required=False, widget=FileInput,label='Elegir imagen')
        fields = [
            'title', 'message'
        ]
        labels = {
            'title': 'Título',
            'message': 'Descripción',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mx-auto font32'}),
            'message': forms.Textarea(attrs={'class': 'storyMessageInput keepWhitespaceFormatting'}),
        }

    def __init__(self, *args, **kwargs):
        super(PetitionForm, self).__init__(*args, **kwargs)
        self.fields['message'].strip = False

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    username = forms.CharField(label='Nombre de usuario',max_length=15)
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
    birthdate = forms.DateField(label='Fecha de nacimiento(Recuerda que si eres menor a 55 años no podrás escribir historias)',widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    biography = forms.CharField(widget=forms.Textarea, label='biografía(pequeña descripción sobre tu persona)-Opcional',
                                required=False)
    profileImage = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'file-field '}), label='Foto de perfil -Opcional')

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

class CommentForm(forms.ModelForm):
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'storyMessageInput keepWhitespaceFormatting'}), label='Comentario')
    class Meta:
        model = Comment
        fields = [
            'message'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'class': 'storyMessageInput keepWhitespaceFormatting'}),
        }