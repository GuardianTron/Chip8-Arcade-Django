from chip8.models.fields import Chip8FileField
from chip8.models.validators import MaxFilesizeValidator
from django.db import models

class Chip8TestModel(models.Model):
    file = Chip8FileField(upload_to="chip8_test")

class FileSizeValidatorModel(models.Model):
    file = models.FileField(upload_to="chip8_test",validators=[MaxFilesizeValidator(100)])

class FileSizeValidatorInvalidFieldModel(models.Model):
    file = models.TextField(validators=[MaxFilesizeValidator(100)])

# Chip 8 fields double the file size during
# format conversion process.  This will be used to 
# test whether or not the file size validator is 
# run after files have been saved

class FileSizeValidatorCheckSaved(models.Model):
    file = Chip8FileField(upload_to="chip8_test",validators=[MaxFilesizeValidator(100,True)])

class FileSizeValidatorNoCheckSaved(models.Model):
    file = Chip8FileField(upload_to="chip8_test",validators=[MaxFilesizeValidator(100)])
