from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . emailbackend import EmailBackEnd


# Create your views here.
def demo_page(request):
    return render(request, 'spve/demo_page.html')


def login_page(request):
    return render(request, 'spve/login_page.html')


def logged_in(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None:
            login(request, user)
            return HttpResponse("Email: "+request.POST.get("email")+"Password: "+request.POST.get("password"))
        else:
            return HttpResponse("Invalid Login")


def user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+"usertype: "+request.user.user_type)
    else:
        return HttpResponse("Please Log In First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login")
