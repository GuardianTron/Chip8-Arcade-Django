from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.core.serializers import serialize
import json
from .models import Chip8GameModel

# Create your views here.

class GameListView(ListView):
    model = Chip8GameModel
    queryset = Chip8GameModel.objects.all()

    def get(self, response, *args, **kwargs):
        qs = self.get_queryset()
        json_output = serialize('json',qs)
        return HttpResponse(json_output)

class GameView(DetailView):
    model = Chip8GameModel

    def get(self, response, *args, **kwargs):
        game = self.get_object()
        json_output = serialize('json',[game],fields=['title','description','keys','buttons','file'])

        return HttpResponse(json_output)

