import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MassagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add("abc%s" % (self.scope['user'].id), self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        await self.channel_layer.group_discard("abc%s" % (self.scope['user'].id), self.channel_name)
