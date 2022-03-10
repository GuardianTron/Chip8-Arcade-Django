from django.db import models
from django.core.validators import MaxLengthValidator
from .fields import Chip8FileField
from .validators import MaxFilesizeValidator


class Chip8GameModel(models.Model):
    '''Represents one chip 8 game'''
    class Meta:
        verbose_name = "Chip 8 Game"
        verbose_name_plural = "Chip 8 Games"
        


    file = Chip8FileField(blank=False,upload_to='games',validators=[MaxFilesizeValidator(4096)])
    description = models.TextField(null=True,blank=False,max_length=2000,validators=[MaxLengthValidator(2000)])
    title = models.CharField(blank=False,null=False,default="Please add a title.",max_length=100)
    author = models.CharField(blank=True,null=True,max_length=100)
