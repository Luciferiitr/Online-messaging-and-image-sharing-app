import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from .models import *

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)


        other_user = self.scope['url_route']['kwargs']['phone']
        me = self.scope['user']
        # print(other_user, me)
        self.chat_room = 'chat1';
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        await self.send({
            'type' : 'websocket.accept'
        })

    async def websocket_receive(self , event):
        print('receive', event)
        msg = event['text']
        data = json.loads(msg)
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type' : 'chat_message',
                'text' : json.dumps(data)
            }
        )

    async def chat_message(self, event):
        await self.send({
            'type' : 'websocket.send',
            'text' : event['text']
        })
    async def websocket_disconnect(self , event):
        print('disconnected', event)
