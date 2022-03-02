from django.db import models
from .fields import Chip8FileField


class Chip8GameModel(models.Model):
    '''Represents one chip 8 game'''

    file = Chip8FileField(upload_to='games')
