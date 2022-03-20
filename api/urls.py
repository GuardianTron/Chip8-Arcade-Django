from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameListView,GameView

urlpatterns = [
    path('',GameListView.as_view(),name="list_json"),
    path('<int:pk>',GameView.as_view(),name="game_json"),
]

urlpatterns = format_suffix_patterns(urlpatterns)