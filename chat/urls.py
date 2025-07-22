from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.lobby, name="chat_lobby"),
    path("room/<str:room_name>/", views.room, name="chat_room"),
    path("upload/", views.upload_file, name="upload_file"),
    path("download/<str:filename>/", views.download_file, name="download_file"),
    path("messages/<str:room_name>/", views.get_messages, name="get_messages"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
