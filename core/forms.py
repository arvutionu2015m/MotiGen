from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

class CVForm(forms.Form):
    cv_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), label="Sisesta oma CV")

class CVUploadForm(forms.Form):
    cv_file = forms.FileField(
        label="Lae üles CV (.pdf või .docx)",
        help_text="Toetatud vormingud: .pdf ja .docx"
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class CVForm(forms.Form):
    cv_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), label="Sisesta oma CV")
