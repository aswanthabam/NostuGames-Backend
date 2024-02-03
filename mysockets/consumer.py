from channels.generic.websocket import AsyncWebsocketConsumer
import json
from db.asyncdb import BingoManager

class BingoGame(AsyncWebsocketConsumer):
    async def end_group(self, group_name):
        await self.channel_layer.group_send(
                self.room.code,
                {
                    "type": "room.message",
                    "message": f"{self.member.name} left the room",
                }
            )
        await self.channel_layer.group_discard(group_name, self.channel_name)

    async def connect(self):
        self.room = self.scope.get('room')
        self.member = self.scope.get('member')
        connect_message = self.scope.get("connect_message")
        error_exit = self.scope.get("error_exit")

        await self.accept()
        if error_exit:
            await self.send(text_data=json.dumps({
                "type":"error",
                "message":error_exit
            }))
            await self.close()
            return
        if not self.room:
            await self.send(text_data=json.dumps({
                "type":"error",
                "message":"Invalid Room"
            }))
            await self.close()
        await self.channel_layer.group_add(self.room.code, self.channel_name)
        if connect_message:
            await self.channel_layer.group_send(
                self.room.code,
                {
                    "type": "room.message",
                    "message": connect_message,
                }
            )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        _type = data.get("type")
        if not _type:
            await self.send(text_data=json.dumps({
                "type":"error",
                "message":"Invalid Message Type"
            }))
            return
        if _type == "message":
            await self.channel_layer.group_send(
                self.room.code,
                {
                    "type": "room.message",
                    "message": data.get("message"),
                }
            )
        elif _type == "game_move":
            bingo = await BingoManager.bingo_get_game(self.room)
            if not bingo:
                bingo = await BingoManager.bingo_create_game(self.room,next_move=self.member)
            # print(await BingoManager.bingo_get_next_move(bingo),self.member.id)
            if str(bingo.next_move.id) != str(self.member.id):
                await self.send(text_data=json.dumps({
                    "type":"error",
                    "message":"Not your turn"
                }))
                return
            if await BingoManager.bingo_is_game_over(bingo):
                await self.send(text_data=json.dumps({
                    "type":"error",
                    "message":"Game Over"
                }))
                return
            if data.get("message") in bingo.used_numbers:
                await self.send(text_data=json.dumps({
                    "type":"error",
                    "message":"Number already used"
                }))
                return
            await BingoManager.bingo_add_move(bingo,data.get("message"),self.member)
            await self.channel_layer.group_send(
                self.room.code,
                {
                    "type": "game.move",
                    "message": data.get("message"),
                }
            )
    
    async def room_message(self, event):
        await self.send(text_data=json.dumps({
            "type":"message",
            "message":event["message"]
        }))

    async def game_move(self, event):
        await self.send(text_data=json.dumps({
            "type":"game_move",
            "message":event["message"]
        }))
    
    # async def disconnect(self, close_code):
    #     # Leave room group

    #     await self.end_group(self.room.code)
    #     pass