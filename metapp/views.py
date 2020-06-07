from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages


# Create your views here.
def demo(request):
    return render(request, "dashboard/index.html")

# View to display the General Loginpage of the app
def loginPage(request):
    return render(request, "auth/login.html")


def logoutPage(request):
    logout(request)
    return HttpResponseRedirect("login")


def profilePage(request):
    return render(request, "auth/profile.html")


# Function for handling the login
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<p>Method Not Allowed</p>")
    else:
        user = EmailBackEnd.authenticate(request, username = request.POST.get("loginEmail"), password = request.POST.get('loginPassword'))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/adminHome')  
            elif user.user_type == "2":
                return HttpResponse("Welcome Staff")
            else:
                return HttpResponse("Welcome Student")

        else:
            messages.error(request, "Invalid Login Details")
            return redirect("login")
        