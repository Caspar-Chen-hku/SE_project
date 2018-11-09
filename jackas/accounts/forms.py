from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, help_text='Please enter a unique name.')
    first_name = forms.CharField(max_length=50, required=True, help_text='')
    last_name = forms.CharField(max_length=50, required=True, help_text='')
    email = forms.EmailField(max_length=50, help_text='Please enter a valid email address.')
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="More than 8 characters of numbers and symbols")
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")
    ROLE_CHOICES = (('CM', 'Clinic Manager'), ('WP', 'Warehouse Personnel'), ('D', 'Dispacher'))
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role", required=True)
    clinic_name = forms.CharField(max_length=100, required=False, help_text="Required for clinic managers.")
    clinic_address = forms.CharField(max_length=200, required=False, help_text="Required for clinic managers.")    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'clinic_name', 'clinic_address')