from django.db import models
from django.core.validators import MaxLengthValidator,MaxValueValidator
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


class KeyConfig(models.Model):

    '''Links chip 8 keys to physical keyboard keys using Javascript KeyboardEvent.code'''

    class Meta:
        verbose_name = "Key Configuration"
        verbose_name_plural = "Key Configuration"
        constraints = [models.UniqueConstraint(fields=["game_id","keyboard_code"],name="unique_keyboard_key")]
    
    game_id = models.ForeignKey(Chip8FileField,on_delete=models.CASCADE,related_name='keys')
    chip8_key = models.PositiveSmallIntegerField(verbose_name="Chip 8 Key",validators=[MaxValueValidator(15)])
    keyboard_code = models.CharField(verbose_name="Javascript Keyboard Code",max_length=20)

