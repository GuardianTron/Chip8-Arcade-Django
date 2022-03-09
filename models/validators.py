from xmlrpc.client import Boolean
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.db.models.fields.files import FieldFile

@deconstructible
class MaxFilesizeValidator:
    '''
        Tests the maximum allowed file size during upload.  
        By default, it does not check the size of files that have already been saved. 
    
    '''
    def __init__(self,max_size_bytes:int=4096,check_committed:Boolean=False):
        self._max_size_bytes = max_size_bytes
        self._check_committed = check_committed
    def __call__(self,value):
        if not isinstance(value,FieldFile):
            raise TypeError(f"Validator may only be attached to FileField instances. Attached to field of type {type(value)}")
        if (self._check_committed or not value._committed) and value.size > self._max_size_bytes:
            raise ValidationError(f"The uploaded file exceeds of the size limit of {self._max_size_bytes} bytes. File is {value.size} bytes.")
