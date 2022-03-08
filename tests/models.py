from chip8.models.fields import Chip8FileField
from django.db import models

class Chip8TestModel(models.Model):
    file = Chip8FileField(upload_to="chip8_test")