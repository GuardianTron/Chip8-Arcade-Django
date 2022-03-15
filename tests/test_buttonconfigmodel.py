from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from chip8.models import Chip8GameModel, ButtonConfigModel


class ButtonConfigModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        cls.game = Chip8GameModel.objects.create(file=SimpleUploadedFile(name="the game",content=b"a"*255),
                                         author="me myself and I",
                                         description="You Lose!",
                                         title="The Game"
                                        )
        cls.game.buttons.create(chip8_key=1,button_id="button_a")

    def test_no_duplicate_button_ids(self):

        '''Make sure buttons cannot be mapped to mulitple chip 8 keys'''
        with self.assertRaises(IntegrityError):
            self.game.buttons.create(chip8_key=2,button_id="button_a")
    
    def test_multiple_button_ids_for_chip8_key(self):
        self.game.buttons.create(chip8_key=1,button_id="button_b")

    def test_chip8_key_range(self):
        key_model = self.game.buttons.first()
        key_model.full_clean() #correct
        key_model.chip8_key = 15 
        key_model.full_clean()

        key_model.chip8_key = 16
        with self.assertRaises(ValidationError):
            key_model.full_clean()

        key_model.chip8_key = -1
        with self.assertRaises(IntegrityError):
            key_model.save()
