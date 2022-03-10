from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from .models import FileSizeValidatorInvalidFieldModel,FileSizeValidatorModel,FileSizeValidatorCheckSaved,FileSizeValidatorNoCheckSaved

class FileSizeValidatorTests(TestCase):

    def test_invalid_field_type(self):
        test_model = FileSizeValidatorInvalidFieldModel(file="I'm not a file.")
        with self.assertRaises(TypeError):
            test_model.full_clean()

    def test_valid_file_size(self):
        file = SimpleUploadedFile(name="Immaproperfile",content=b"a"*100)
        test_model = FileSizeValidatorModel(file=file)
        test_model.full_clean()

    def test_invalid_file_size(self):
        file=SimpleUploadedFile(name="Immatoobigfile",content=b"a"*101)
        test_model = FileSizeValidatorModel(file=file)
        with self.assertRaises(ValidationError):
            test_model.full_clean()

    def test_checks_updated_upload(self):
        file = SimpleUploadedFile(name="I'm just right.",content=b"a"*100)
        test_model = FileSizeValidatorModel(file=file)
        test_model.full_clean()
        test_model.save()
        test_model.file = SimpleUploadedFile(name="I'mtoobig",content=b"a"*101)
        with self.assertRaises(ValidationError):
            test_model.full_clean()

    def test_no_check_saved(self):
        # File size doubles when being saved,
        # so if a check is being performed, this
        # test will fail the second call to full_clean
        file = SimpleUploadedFile(name='Immaproperfile',content=b"a"*100)
        test_model = FileSizeValidatorNoCheckSaved(file=file)
        test_model.full_clean()
        test_model.save()
        test_model.full_clean()

    def test_check_saved(self):
        # File size doubles when being saved,
        # so if check is performed after save,
        # it should throw a validation error.
        file = SimpleUploadedFile(name="Immaproperfilebutillbetoobig",content=b"a"*100)
        test_model = FileSizeValidatorCheckSaved(file=file)
        test_model.full_clean()
        test_model.save()
        with self.assertRaises(ValidationError):
            test_model.full_clean()

    

    
