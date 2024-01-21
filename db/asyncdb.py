
from db.models import *
from channels.db import database_sync_to_async

class BingoManager:
    @staticmethod
    @database_sync_to_async
    def bingo_get_game(room:GameRoom) -> Bingo:
        bingo = Bingo.objects.filter(room=room).prefetch_related('next_move').first()
        return bingo

    @staticmethod
    @database_sync_to_async
    def bingo_is_game_over(bingo:Bingo) -> bool:
        return bingo.game_over

    @staticmethod
    @database_sync_to_async
    def bingo_create_game(room:GameRoom,next_move:GameMember) -> Bingo:
        return Bingo.objects.create(room=room,next_move=next_move)

    @staticmethod
    @database_sync_to_async
    def bingo_get_members(bingo:Bingo) -> list[GameMember]:
        return GameMember.objects.filter(room=bingo.room)

    @staticmethod
    @database_sync_to_async
    def bingo_add_move(bingo:Bingo,move:str,current:GameMember) -> None:
        bingo.used_numbers.append(move)
        bingo.next_move = GameMember.objects.filter(room=bingo.room).exclude(id=current.id).first()
        bingo.save()

    @staticmethod
    @database_sync_to_async
    def create_bingo_game(room:GameRoom) -> Bingo:
        return Bingo.objects.create(room=room)
    
    @staticmethod
    @database_sync_to_async
    def bingo_set_next_move(bingo:Bingo,member:GameMember) -> None:
        bingo.next_move = member
        bingo.save()