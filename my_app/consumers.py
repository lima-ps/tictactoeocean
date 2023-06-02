import random
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from my_app.helpers import *
from my_app.models import Room
from channels.db import database_sync_to_async



#config of our websocket, also changed at asgi.py after install de app "channels".
#Consumers receive the connection’s scope (scope contain all the information of the resquest. It’s available as self.scope)
class MyappConsumer(AsyncJsonWebsocketConsumer):
    
    board = {0: '', 1: '', 2: '',  
             3: '', 4: '', 5: '', 
             6: '', 7: '', 8: ''}
    
     # Called on connection.
    async def connect(self):
        #print(self.scope['url_route']['kwargs']['id']) #kwargs are dictionary arguments that receives "key:args (ex. id:14)"
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.group_name = f'group_{self.room_id}'
        print(f'group_name>> {self.group_name}')
        
        try:
            if (len(self.channel_layer.groups[self.group_name]) >= 2):
                await self.accept()
                await self.send_json({
                    "event": "show_error",
                    "error": "This room is full!"
                })
                return await self.close(1)
        except KeyError:
            pass
        
        # To accept the connection call:
        await self.accept()
        print(f'final group {self.channel_name}')
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(f'self.channel_layer.groups>> {self.channel_layer.groups}')
        if (len(self.channel_layer.groups[self.group_name]) == 2):
            #convert the dictionary to a list to access easily just the key
            tmpGroup = list(self.channel_layer.groups[self.group_name])
            first_player = random.choice(tmpGroup)
            tmpGroup.remove(first_player)
            final_group = [first_player, tmpGroup[0]]
            print(f'final group {final_group}')

            for i, channel_name in enumerate(final_group):
                await self.channel_layer.send(channel_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "game_start",
                        "board": self.board,
                        "myTurn": True if i == 0 else False 
                    }
                })
            

    # Called with either text_data or bytes_data for each frame
    async def receive_json(self, content, **kwargs):
        print(f'content>> {content}')
        
        if(content["event"] == "boardData_send"):

            winner = checkWin(content['board'])
            
            if(winner):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "won",
                        "board": content['board'],
                        "myTurn": False,
                        "winner": winner,
                    }
                })
            if(isDraw(content['board'])):
                return await self.channel_layer.group_send(self.group_name, {
                    "type": "gameData.send",
                    "data": {
                        "event": "draw",
                        "board": content['board'],
                        "myTurn": False,
                    }
                })
                
            else: 
            
                for channel_name in self.channel_layer.groups[self.group_name]:
                    await self.channel_layer.send(channel_name, {
                        "type": "gameData.send",
                        "data": {
                            "event": "boardData_send",
                            "board": content['board'],
                            "myTurn": False if self.channel_name==channel_name else True
                        }
                    })
                    
        elif(content["event"] == "restart"):
            if (len(self.channel_layer.groups[self.group_name]) == 2):
                #convert the dictionary to a list to access easily just the key
                tmpGroup = list(self.channel_layer.groups[self.group_name])
                print(tmpGroup)
                first_player = random.choice(tmpGroup)
                tmpGroup.remove(first_player)
                final_group = [first_player, tmpGroup[0]]
                print(final_group)

                for i, channel_name in enumerate(final_group):
                    await self.channel_layer.send(channel_name, {
                        "type": "gameData.send",
                        "data": {
                            "event": "game_start",
                            "board": self.board,
                            "myTurn": True if i == 0 else False 
                        }
                    })
                    
    def getRoomId(self):
        return self.scope['url_route']['kwargs']['id']
        
     # Called when the socket closes
    async def disconnect(self, code):
        
        def getRoomId(r):
            return r
        
        if(code == 1):
            return
        if(len(self.channel_layer.groups[self.group_name]) <= 1 ):
            room = await database_sync_to_async(getRoomId)(self.scope['url_route']['kwargs']['id'])
            roomId = await database_sync_to_async(Room.objects.get)(roomNumber=room)
            await database_sync_to_async(roomId.delete)()
            
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(self.group_name, {
            "type": "gameData.send",
            "data": {
                "event": "opponent_left",
                "board": self.board,
                "myTurn": False,
            }
        })
    
    async def gameData_send(self, context):
        await self.send_json(context['data'])