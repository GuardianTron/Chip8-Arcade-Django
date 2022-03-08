from django.db import models
from .fields import Chip8FileField


class Chip8GameModel(models.Model):
    '''Represents one chip 8 game'''

    file = Chip8FileField(upload_to='games')
    description = models.TextField(null=True,blank=True,max_length=2000)
    title = models.CharField(blank=False,null=False,default="Please add a title.",max_length=500)
    author = models.CharField(blank=True,null=True,max_length=100)
