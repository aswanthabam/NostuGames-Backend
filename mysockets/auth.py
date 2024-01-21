from channels.db import database_sync_to_async
from db.asyncdb import *
import  urllib.parse

class RoomAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query = urllib.parse.parse_qs(scope['query_string'].decode())
        room_code = query.get('room_code')
        room_code = room_code[0] if room_code else None
        game=query.get("game",None)
        game = game[0] if game else None
        user_id = query.get("user_id",None)
        user_id = user_id[0] if user_id else None
        connect_message = None
        error_exit = None
        # Check room code
        if not room_code:
            error_exit = "Invalid Room Code provided!"
            scope['error_exit'] = error_exit
            return await self.app(scope, receive, send)
        room = await RoomManager.get_room(room_code,game=game)

        if not room:
            if not game or game not in ["bingo"]:
                error_exit = "Invalid Game provided!"
                scope['error_exit'] = error_exit
                return await self.app(scope, receive, send)
            room = await RoomManager.create_room(room_code,game) # Create room if not exists
            if game == "bingo":
                await BingoManager.create_bingo_game(room)
            connect_message = f"Created Room for {game}"
            
        if user_id:
            member = await RoomManager.get_member(room,user_id)
            if not member:
                error_exit = "Invalid User Id provided!"
                scope['error_exit'] = error_exit
                return await self.app(scope, receive, send)
        else:
            name = query.get("name")
            if not name:
                error_exit = "Invalid Name provided!"
                scope['error_exit'] = error_exit
                return await self.app(scope, receive, send)
            name = name[0]
            member = await RoomManager.add_member(room,name)
            connect_message = f"{name} Joined the room" if not connect_message else connect_message
        if game == "bingo":
            bingo = await BingoManager.bingo_get_game(room)
            if bingo.game_over:
                error_exit = "Game is already over"
                scope['error_exit'] = error_exit
                return await self.app(scope, receive, send)
            if not bingo.next_move:
                await BingoManager.bingo_set_next_move(bingo,member)
                print("NEXT MOVE : ",bingo.next_move)
            scope['bingo'] = bingo
        scope['room'] = room
        scope['member'] = member
        scope['connect_message'] = connect_message
        return await self.app(scope, receive, send)