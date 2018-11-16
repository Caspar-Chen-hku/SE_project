from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignUpFormCM, AuthTokenForm
from asp.models import User, Clinic, Category, Token
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail
import random

def authentication(request):
    if request.method == 'POST':
        token = request.POST['token']
        if Token.objects.filter(token_string=token).exists():
            Token.objects.filter(token_string=token).delete()
            if token[0:2] == "01":
                return redirect('/accounts/clinic_manager/register')
            elif token[0:2] == "02":
                return redirect('/accounts/warehouse_personnel/register')
            elif token[0:2] == "03":
                return redirect('/accounts/dispatcher/register')
            else:
                return redirect('/accounts/auth_token')
        else:
            return redirect('/accounts/auth_token')
    else:
        form = AuthTokenForm()
        print(form)
        return render(request, 'auth_token.html', {'form': form})

def signup_cm(request):
    if request.method == 'POST':
        form = SignUpFormCM(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            new_user = User()
            new_user.username = username
            new_user.password = raw_password
            new_user.firstname = form.cleaned_data.get('first_name')
            new_user.lastname = form.cleaned_data.get('last_name')
            new_user.email = form.cleaned_data.get('email')
            new_user.role = 'CM'
            try:
                clinic = Clinic.objects.get(clinic_name = form.cleaned_data.get('clinic_name'))
                new_user.clinic_id = clinic
            except Clinic.DoesNotExist:
                new_clinic = Clinic()
                new_clinic.clinic_name = form.cleaned_data.get('clinic_name')
                new_clinic.clinic_address = form.cleaned_data.get('clinic_address')
                new_clinic.save()
                new_user.clinic_id = new_clinic
            new_user.save()
            
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            login_user = User.objects.get(username = username)
            userid = login_user.pk

            category_id = Category.objects.get(category_name='IV Fluids').pk
            return redirect('/asp/clinic_manager/'+str(userid)+'/home/'+str(category_id))
    else:
        form = SignUpFormCM()
    return render(request, 'signup.html', {'form': form, 'role': 'Clinic Manager'})

def signup_wp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            new_user = User()
            new_user.username = username
            new_user.password = raw_password
            new_user.firstname = form.cleaned_data.get('first_name')
            new_user.lastname = form.cleaned_data.get('last_name')
            new_user.email = form.cleaned_data.get('email')
            new_user.role = 'WP'

            new_user.save()
            
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            login_user = User.objects.get(username = username)
            userid = login_user.pk

            return redirect("/asp/warehouse_personnel/"+str(userid)+"/home")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'role': 'Warehouse Personnel'})

def signup_d(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            new_user = User()
            new_user.username = username
            new_user.password = raw_password
            new_user.firstname = form.cleaned_data.get('first_name')
            new_user.lastname = form.cleaned_data.get('last_name')
            new_user.email = form.cleaned_data.get('email')
            new_user.role = 'D'
            
            new_user.save()
            
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            login_user = User.objects.get(username = username)
            userid = login_user.pk

            return redirect('/asp/dispatcher/'+str(userid)+'/home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'role': 'Dispatcher'})

@csrf_exempt
def adminSendToken(request):
    if request.method == 'POST':
        email = request.POST['email']
        role = request.POST['role']
        if role == 'cm':
            token = "01" + str(random.randint(1000,9999))
        elif role == 'wp':
            token = "02" + str(random.randint(1000,9999))
        else:
            token = "03" + str(random.randint(1000,9999))
        token_to_add = Token(token_string = token)
        token_to_add.save()
        subject = 'AS-P Token'
        body = "Token is: " + token + "\nRole: " + role + "\nPlease use the token to register.\n"
        from_asp = 'admin@asp.com'

        send_mail(subject, body, from_asp, [email], fail_silently=False)
        return redirect('/accounts/admin')
    else:
        return render(request, 'send_token.html', {})