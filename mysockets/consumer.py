from channels.generic.websocket import AsyncWebsocketConsumer
import json, urllib.parse
from asgiref.sync import async_to_sync

class DataAccessor(AsyncWebsocketConsumer):
    
    async def end_group(self, group_name):
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def connect(self):
        await self.accept()
        
    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data="dakd")
        
    async def disconnect(self, close_code):
        pass