from chip8.models import Chip8GameModel,KeyConfigModel
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

class TestKeyConfigModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game = Chip8GameModel.objects.create(file=SimpleUploadedFile(name="the game",content=b"a"*255),
                                                 author="me myself and I",
                                                 description="You Lose!",
                                                 title="The Game"
                                                )
        cls.game.keys.create(chip8_key=1,keyboard_code="Backspace")

    def test_no_duplicate_keyboard_codes(self):
        '''Make sure that a keyboard key cannot be mapped twice.'''
        with self.assertRaises(IntegrityError):
            self.game.keys.create(chip8_key=2,keyboard_code="Backspace")
    
    def test_multiple_keyboard_codes_for_chip8_key(self):
        '''Make sure chip 8 keys can be mapped to multiple keys.'''
        self.game.keys.create(chip8_key=1,keyboard_code="ArrowLeft")


    def test_chip8_key_range(self):
        key_model = self.game.keys.first()
        key_model.full_clean() #correct
        key_model.chip8_key = 15 
        key_model.full_clean()

        key_model.chip8_key = 16
        with self.assertRaises(ValidationError):
            key_model.full_clean()

        key_model.chip8_key = -1
        with self.assertRaises(IntegrityError):
            key_model.save()

    def _invalid_keyboard_codes(self,key_model,value):
        key_model.keyboard_code = value
        with self.assertRaises(ValidationError):
            key_model.full_clean()

    def test_keyboard_code_regex(self):
        #correct examples
        key_model = self.game.keys.first()
        key_model.keyboard_code = "Backspace"
        key_model.full_clean()

        key_model.keyboard_code = "ArrowLeft"
        key_model.full_clean()

        key_model.keyboard_code = "F10"
        key_model.full_clean()

        #lowercase first letter
        self._invalid_keyboard_codes(key_model,'backspace')

        #spaces
        self._invalid_keyboard_codes(key_model,' Backspace')
        self._invalid_keyboard_codes(key_model,'Backspace ')
        self._invalid_keyboard_codes(key_model,'Back space')

        #numbers
        self._invalid_keyboard_codes(key_model,'3Backspace')
        self._invalid_keyboard_codes(key_model,'Back3space')
        self._invalid_keyboard_codes(key_model,'Backspace333')


        
    