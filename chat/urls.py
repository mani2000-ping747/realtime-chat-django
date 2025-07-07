from django.urls import path
from . import views

urlpatterns = [
    path("", views.lobby, name="chat_lobby"),  # chat lobby view
    path("room/<str:room_name>/", views.room, name="chat_room"),
]
