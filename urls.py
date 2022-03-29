from django.urls import path,include


from .views import player

app_name = "chip8"

urlpatterns = [
    path('',player,name='player'),
    path('api/',include('chip8.api.urls')),

]