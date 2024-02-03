from rest_framework import serializers
from db.models import GameRoom, GameMember
class GameRoomSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    def get_members(self,obj):
        members = [{
            'name':x.name,
            'status':x.status
        } for x in GameMember.objects.filter(room__code=obj.code)]
        return members

    class Meta:
        fields = [
            'id',
            'code',
            'members_count',
            'game',
            'members'
        ]
        model = GameRoom
