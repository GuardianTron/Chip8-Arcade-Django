from django.shortcuts import render

def player(request):
    return render(request,'chip8/player.html')


