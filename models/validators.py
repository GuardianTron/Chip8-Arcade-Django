from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.db.models.fields.files import FieldFile

@deconstructible
class MaxFilesizeValidator:

    def __init__(self,max_size_bytes:int=4096):
        self._max_size_bytes = max_size_bytes

    def __call__(self,value):
        if not isinstance(value,FieldFile):
            raise TypeError(f"Validator may only be attached to FileField instances. Attached to field of type {type(value)}")
        if value.size > self._max_size_bytes:
            raise ValidationError(f"The uploaded file exceeds of the size limit of {self._max_size_bytes} bytes.")
