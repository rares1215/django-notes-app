from django.shortcuts import render,redirect
from django.shortcuts import render,redirect
from .forms import CustomLoginForm,CustomRegisterForm
from django.contrib.auth import login,logout
from django.contrib import messages


# Create your views here.

def register_user(request):
    if request.method=='POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            login(request,form.save())
            messages.success(request,"Account created successfully")
            return redirect('notes:notes_page')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register_page.html',{'form':form})

def login_user(request):
    if request.method =='POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            messages.success(request,"You are now logged in")
            return redirect("notes:notes_page")
    else:
        form = CustomLoginForm()
    return render(request, 'users/login_user.html', {'form':form})

def logout_user(request):
    if request.method =='POST':
        logout(request)
        messages.warning(request,"You Logged out!")
        return redirect("users:login-user")
