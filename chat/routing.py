from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<course_id>\d+)/$', consumers.CourseChatConsumer.as_asgi()),
] #URL for websocket is ws/chat/(the course ID); this allows it to adjust automatically if new courses are added