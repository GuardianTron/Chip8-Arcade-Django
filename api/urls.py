from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GameListView,GameView

urlpatterns = [
    path('',GameListView.as_view()),
    path('<int:pk>',GameView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)