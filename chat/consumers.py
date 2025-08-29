from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import ChatMessage, Course
from accounts.models import User

class CourseChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"Connecting WebSocket for course {self.scope['url_route']['kwargs']['course_id']}")
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f"chat_course_{self.course_id}"

        #Join course chat channel
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        #Exit channel when necessary
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    #Message is received by other users in chat live
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user'].username if self.scope['user'].is_authenticated else "Anonymous"

        await self.save_message(sender, self.course_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
        
    @sync_to_async
    def save_message(self, sender, course_id, message): #Save message for Chat History

        course = Course.objects.get(id=course_id)
        user = User.objects.get(username=sender)

        return ChatMessage.objects.create(sender=user, course=course, message=message)