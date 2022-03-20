from django.urls import path
from .views import GameListView,GameView

urlpatterns = [
    path('',GameListView.as_view()),
    path('<int:pk>',GameView.as_view()),
]