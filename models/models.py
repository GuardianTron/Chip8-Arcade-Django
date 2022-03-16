from tabnanny import verbose
from django.db import models
from django.core.validators import MaxLengthValidator,MaxValueValidator,RegexValidator
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

    def __str__(self):
        return self.title


class AbstractConfigModel(models.Model):
    '''Acts as the base model for all configuration classes.'''
    
    class Meta:
        abstract=True


    chip8_key = models.PositiveSmallIntegerField(verbose_name="Chip 8 Key",validators=[MaxValueValidator(15)])



class KeyConfigModel(AbstractConfigModel):

    '''Links chip 8 keys to physical keyboard keys using Javascript KeyboardEvent.code'''

    class Meta:
        verbose_name = "Key Configuration"
        verbose_name_plural = "Key Configuration"
        constraints = [models.UniqueConstraint(fields=["game_id","keyboard_code"],name="unique_keyboard_key")]
    
    game_id = models.ForeignKey(Chip8GameModel,on_delete=models.CASCADE,related_name='keys')
    keyboard_code = models.CharField(verbose_name="Javascript Keyboard Code",max_length=20,validators=[RegexValidator('^[A-Z][A-Za-z]*[0-9]{0,2}$')])


class ButtonConfigModel(AbstractConfigModel):

    '''Links chip 8 keys to button icons for touch controls'''

    class Meta:
        verbose_name = "Button Configuration"
        verbose_name_plural = "Button Configuration"
        constraints = [models.UniqueConstraint(fields=['game_id','button_id'],name="unique_button_key")]

    BUTTON_CHOICES = [
        ('dir_left','D Pad - Left'),
        ('dir_right','D Pad - Right'),
        ('dir_down','D Pad - Down'),
        ('dir_up','D Pad - Up'),
        ('button_a','A Button'),
        ('button_b','B Button'),
        ('button_c','C Button'),
        ('button_x','X Button'),
        ('button_y','Y Button'),
        ('button_z','Z Button')
    ]


    game_id = models.ForeignKey(Chip8GameModel,on_delete=models.CASCADE,related_name='buttons')
    button_id = models.CharField(verbose_name="Button Id",max_length=10, choices=BUTTON_CHOICES, default='dir_left')