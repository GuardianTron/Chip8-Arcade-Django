from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import FileSizeValidatorInvalidFieldModel,FileSizeValidatorModel

class FileSizeValidatorTests(TestCase):

    def test_invalidfieldtype(self):
        test_model = FileSizeValidatorInvalidFieldModel(file="I'm not a file.")
        with self.assertRaises(TypeError):
            test_model.full_clean()

    def test_validfilesize(self):
        file = SimpleUploadedFile(name="Immaproperfile",content=b"a"*100)
        test_model = FileSizeValidatorModel(file=file)
        test_model.full_clean()

    def test_invalidfilesize(self):
        file=SimpleUploadedFile(name="Immatoobigfile",content=b"a"*101)
        test_model = FileSizeValidatorModel(file=file)
        with self.assertRaises(ValidationError):
            test_model.full_clean()

    

    
