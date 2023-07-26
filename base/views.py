from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request,'base/index.html')

def signUp(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Registration successful.")
            return redirect("dashboard")
        messages.error(request,"Unsuccessful registration. Invalid Inforation.")
    form=UserRegistrationForm()
    context={'form':form}
    return render(request,'base/signUp.html',context)

def signIn(request):
    if request.method=="POST":
        form=UserLoginForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are now logged om as {username} ")
                return redirect("index")
            else:
                messages.error(request,"Invalid Username and Password.")
        else:
            messages.error(request,"Invalid username and password")

    form=UserLoginForm()
    context={'form':form}
    return render(request, "base/signIn.html",context)

def signOut(request):
    logout(request)
    messages.info(request,"You have logged out successfully")
    return redirect("index")

def userDashboard(request):
    Username=request.user.first_name
    context={'Username':Username}
    return render(request,'base/UserDashboard.html',context)

def createMeeting(request):
    UserFirstName=request.user.first_name
    UserLastName=request.user.last_name
    UserFullName=UserFirstName+UserLastName

    context={'UserFullName':UserFullName}
    return render(request,'base/visalogs.html',context)

def joinMeeting(request):
    if request.method=='POST':
        roomID=request.POST['roomID']
        return redirect("/createMeeting?roomID=" +roomID)
    return render(request,'base/joinMeeting.html')