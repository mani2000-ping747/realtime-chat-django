# accounts/views.py

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required


@login_required
def lobby(request):
    return render(request, "chat/lobby.html")


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
