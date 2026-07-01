from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from  django.contrib import auth
from . forms import RegistrationForm
# Create your views here
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username = username,password = password)
            if user is not None:
                auth.login(request,user)
            return redirect('home')
    form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'registration/login.html',context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # checks validity of data from the form
        if form.is_valid():
            form.save()
            return redirect('register')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request,'registration/register.html',context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')