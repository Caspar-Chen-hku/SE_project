from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AuthTokenForm(forms.Form):
    token = forms.CharField(max_length=6, required=True, help_text='Enter the token you received.')

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, help_text='Please enter a unique name.')
    first_name = forms.CharField(max_length=50, required=True, help_text='')
    last_name = forms.CharField(max_length=50, required=True, help_text='')
    email = forms.EmailField(max_length=50, help_text='Please enter a valid email address.')
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="More than 8 characters of numbers and symbols")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

CLINIC_CHOICES = [
    (1, "Ap Lei Chau General Out-patient Clinic"),
    (2, "Aberdeen Jockey Club General Out-patient Clinic"),
    (3, "Tai O Jockey Club General Out-patient Clinic"),
    (4, "Sok Kwu Wan General Out-patient Clinic"),
    (5, "Peng Chau General Out-patient Clinic"),
    (6, "Mui Wo General Out-patient Clinic"),
    (7, "North Lamma General Out-patient Clinic")
]

class SignUpFormCM(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, help_text='Please enter a unique name.')
    first_name = forms.CharField(max_length=50, required=True, help_text='')
    last_name = forms.CharField(max_length=50, required=True, help_text='')
    email = forms.EmailField(max_length=50, help_text='Please enter a valid email address.')
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="More than 8 characters of numbers and symbols")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")
    clinic_name = forms.ChoiceField(choices = CLINIC_CHOICES, label="", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'clinic_name')