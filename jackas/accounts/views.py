from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from asp.models import User, Clinic, Category

def signup(request):
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
            new_user.role = form.cleaned_data.get('role')
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

            if login_user.role == 'CM':
                category_id = Category.objects.get(category_name='IV Fluids').pk
                return redirect('/asp/clinic_manager/'+str(userid)+'/home/'+str(category_id))
            elif login_user.role == 'D':
                return redirect('/asp/dispatcher/'+str(userid)+'/home')
            else:
                return redirect("/asp/warehouse_personnel/"+str(userid)+"/home")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})