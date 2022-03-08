from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile,InMemoryUploadedFile,TemporaryUploadedFile,UploadedFile
from .models import Chip8TestModel


class Chip8FileFieldTests(TestCase):

    @classmethod
    def setUpClass(cls):
        content = 255
        cls.file_data = content.to_bytes(1,'big')
        cls.expected_string = str(hex(content))[2:]
        super().setUpClass()

    def _test_by_upload_type(self,upload_class:UploadedFile,msg:str):
        cls = type(self)
        file_model = Chip8TestModel(file=upload_class(name="testsimple",content=cls.file_data))
        file_model.save()
        with file_model.file.open('r') as hex:
            file_string = hex.read()
            self.assertEquals(file_string,cls.expected_string,msg=msg)
  
    def test_simple_upload(self):
        self._test_by_upload_type(SimpleUploadedFile,'Simple upload failed to correctly convert file to hex string.')




