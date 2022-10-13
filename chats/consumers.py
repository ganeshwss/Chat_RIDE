import json
from multiprocessing.resource_sharer import stop
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import ChatModel

class PersonalChatConsumer(AsyncWebsocketConsumer):

    #to  establish connection on the room
    async def connect(self):
        headers = dict(self.scope['headers'])

        # check header information
        if b'authorization' in headers:

                token_name, token_key = headers[b'authorization'].decode().split()
                print(token_key)

                #compare token 
                if token_key == '0e01e3ecbf50299000b906907965649b41ebdb43':

                    self.room_name = self.scope['url_route']['kwargs']['room_name']

                    self.room_group_name = '%s' % self.room_name

                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    await self.accept()

        else:
            self.disconnect()
            



    async def receive(self, text_data=None, bytes_data=None):

        #get data from payload
        text_data_json = json.loads(text_data)

        sender =  text_data_json['sender']
        receiver =  text_data_json['receiver']
        message =  text_data_json['message']
        message_type = text_data_json['message_type']
        platform_name = text_data_json['platform_name']


        await self.save_message(sender,receiver,message,message_type,platform_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender':sender,
                'receiver':receiver,
                'message': message,
                'message_type':message_type,
                'platform_name':platform_name
            }
        )

    async def chat_message(self, event):

        sender = event['sender']
        receiver = event['receiver']
        message = event['message']
        message_type = event['message_type']
        platform_name = event['platform_name']



        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver':receiver,
            'message': message,
            'message_type':message_type,
            'platform_name':platform_name
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    #save message in database
    @database_sync_to_async
    def save_message(self,sender,receiver,message,message_type,platform_name):
        ChatModel.objects.create(
            sender = sender , receiver = receiver,
            message = message , message_type = message_type ,
            platform_name = platform_name, room_name = self.room_group_name)
