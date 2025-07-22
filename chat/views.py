# chat/views.py

import uuid
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import FileResponse, Http404


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


# @csrf_exempt
# def upload_file(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         file = request.FILES["file"]
#         filename = f"{uuid.uuid4().hex}_{file.name}"
#         upload_path = os.path.join(settings.MEDIA_ROOT, "chat_uploads", filename)
#         os.makedirs(os.path.dirname(upload_path), exist_ok=True)

#         with open(upload_path, "wb+") as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)

#         file_url = f"{settings.MEDIA_URL}chat_uploads/{filename}"
#         return JsonResponse({"file_url": file_url})

#     return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_heading = request.POST.get("file_heading", "")

        room_name = request.POST.get("room_name")
        user = request.user

        msg = Message.objects.create(
            user=user, room_name=room_name, file=file, file_heading=file_heading
        )

        return JsonResponse(
            {
                "status": "success",
                "file_url": msg.file.url,
                "file_heading": msg.file_heading,
                "username": msg.user.username,
                "timestamp": msg.timestamp.isoformat(),
            }
        )

    return JsonResponse({"status": "error"}, status=400)


def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, "chat_uploads", filename)

    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, "rb"), as_attachment=True, filename=filename
        )
    else:
        raise Http404(f"File not found: {filename}")


@login_required
def get_messages(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by("timestamp")
    data = [
        {
            "username": msg.user.username,
            "message": msg.content,
            "file_url": msg.file.url if msg.file else "",
            "timestamp": msg.timestamp.strftime("%H:%M"),
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)
