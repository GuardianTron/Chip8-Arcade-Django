from rest_framework.generics import  ListAPIView, RetrieveAPIView
from .serializers import Chip8GameSerializer, Chip8GameListingSerializer
from chip8.models import Chip8GameModel

class GameListView(ListAPIView):
    queryset = Chip8GameModel.objects.all()
    serializer_class = Chip8GameListingSerializer

class GameView(RetrieveAPIView):
    queryset = Chip8GameModel.objects.all()
    serializer_class = Chip8GameSerializer


