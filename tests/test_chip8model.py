from django.core.exceptions import ValidationError
from chip8.models import Chip8GameModel
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class Chip8ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game = Chip8GameModel.objects.create(title="My Game",
                        description="This is my game.",
                        author="teh author",
                        file = SimpleUploadedFile('mygame',content=b"haha")
                    )

    def test_requires_title(self):
        self.game.title=""
        with self.assertRaises(ValidationError):
            self.game.full_clean()

    def test_requires_description(self):
        self.game.description = ""
        with self.assertRaises(ValidationError):
            self.game.full_clean()

    def test_requires_file(self):
        self.game.file = None
        with self.assertRaises(ValidationError):
            self.game.full_clean()

    def test_does_not_require_author(self):
        self.game.author = ''
        self.game.clean()

    def test_author_max_length(self):
        self.game.author = "a"*101
        with self.assertRaises(ValidationError):
            self.game.full_clean()

    def test_title_max_length(self):
        self.game.title = "a"*101
        with self.assertRaises(ValidationError):
            self.game.full_clean()

    def test_description_max_length(self):
        self.game.description="a"*2001
        with self.assertRaises(ValidationError):
            self.game.full_clean()

    def test_passes(self):
        self.game.full_clean()