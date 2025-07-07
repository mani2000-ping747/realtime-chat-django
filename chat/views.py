# chat/views.py

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required
def lobby(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        return redirect("chat_room", room_name=room_name)
    return render(request, "chat/lobby.html")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message


def room(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by("timestamp")
    return render(
        request,
        "chat/room.html",
        {
            "room_name": room_name,
            "username": request.user.username,
            "messages": messages,
        },
    )
