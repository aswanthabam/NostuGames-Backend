from rest_framework.views import APIView
from db.models import GameRoom
from utils.response import CustomResponse
from .serializers import GameRoomSerializer

class GameInfoAPI(APIView):
    def get(self,request):
        room_code = request.GET.get('room_code')
        if room_code is None:return CustomResponse(message="Room code is required!").send_failure_response()
        room = GameRoom.objects.filter(code=room_code).first()
        if not room: return CustomResponse("Invalid room").send_failure_response()
        serializer = GameRoomSerializer(instance=room,many=False)
        return CustomResponse(message="Success",data=serializer.data).send_success_response()

