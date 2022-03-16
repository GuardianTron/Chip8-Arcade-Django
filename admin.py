from django.contrib import admin
from .models import Chip8GameModel,KeyConfigModel,ButtonConfigModel
# Register your models here.
class KeyConfigInline(admin.TabularInline):
    model = KeyConfigModel

class ButtonConfigInline(admin.TabularInline):
    model = ButtonConfigModel

@admin.register(Chip8GameModel)
class Chip8GameAdmin(admin.ModelAdmin):
    inlines=[KeyConfigInline,ButtonConfigInline]