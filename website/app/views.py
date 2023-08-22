from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import create_user_form

# Create your views here.


def home(response):
    return render(response, "app/home.html", {})


def settings(response):
    return render(response, "app/settings.html", {})


def saved(response):
    return render(response, "app/saved.html", {})


def login_page(response):
    if response.method == "POST":
        username = response.POST["username"]
        password = response.POST["password"]
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            messages.success(response, "Logged in")
            return redirect("/")
        else:
            messages.success(response, "There was an error login")
            return render(response, "app/login.html", {})
    else:
        return render(response, "app/login.html", {})


def signup(response):
    if response.method == "POST":
        form = create_user_form(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(response, user)
            messages.success(response, "Sign up successful and logged in")
            return redirect("/")
        else:
            messages.success(response, "Sign up unsuccessful")
            return render(response, "app/signup.html", {"form": form})

    else:
        form = create_user_form()
        return render(response, "app/signup.html", {"form": form})


def logout_user(response):
    logout(response)
    messages.success(response, "Logged out")
    return redirect("/")
