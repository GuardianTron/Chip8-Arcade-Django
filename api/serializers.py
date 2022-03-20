from rest_framework import serializers
from chip8.models import Chip8GameModel,ButtonConfigModel,KeyConfigModel


class ButtonConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonConfigModel
        fields = ['id','chip8_key','button_id']

class KeyConfigSerailizer(serializers.ModelSerializer):
    class Meta:
        model = KeyConfigModel
        fields = ['id','chip8_key','keyboard_code']

class Chip8GameListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chip8GameModel
        fields = ['id','title']

class Chip8GameSerializer(serializers.ModelSerializer):
    buttons = ButtonConfigSerializer(many=True,read_only=True)
    keys = KeyConfigSerailizer (many=True,read_only=True)
    class Meta:
        model = Chip8GameModel
        depth = 1
        fields = ['id','title','author','description','file','buttons','keys']