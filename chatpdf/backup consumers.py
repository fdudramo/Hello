from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
import json
from .models import * 
from .process_ai import ai

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = GroupMessage.objects.create(
            body=body,
            author=self.user, 
            group=self.chatroom 
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
            'body': body,
            'author': self.user.username,
        }
        
        # Send user message to all clients
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

        # Process the AI response only once
        self.process_ai_message(body, message.id)

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_group': self.chatroom
        }

        html = render_to_string("chat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

    def process_ai_message(self, body, message_id):
        ai_response = ai(body)
        ai_user = User.objects.get(username='pdfai')

        ai_message = GroupMessage.objects.create(
            body=ai_response,
            author=ai_user,
            group=self.chatroom
        )

        event = {
            'type': 'ai_message_handler',
            'ai_message_id': ai_message.id,
            'user_message_id': message_id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def ai_message_handler(self, event):
        ai_message_id = event['ai_message_id']
        ai_message = GroupMessage.objects.get(id=ai_message_id)
        context = {
            'message': ai_message,
            'user': self.user,
            'chat_group': self.chatroom
        }

        ai_html = render_to_string("chat/partials/chat_message_p.html", context=context)
        self.send(text_data=ai_html)