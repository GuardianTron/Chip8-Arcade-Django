from django.urls import path,include


app_name = "chip8"

urlpatterns = [
    path('api/',include('chip8.api.urls')),
]