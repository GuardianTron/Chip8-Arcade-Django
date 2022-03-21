from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from chip8.models import Chip8GameModel, ButtonConfigModel, KeyConfigModel

class TestAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game1 = Chip8GameModel.objects.create(
                                            title="Game 1",
                                            description="This is the first game.",
                                            author="anon1",
                                            file=SimpleUploadedFile(name="Game 1",content=b"a"*200)
                                                )

        cls.game2 = Chip8GameModel.objects.create(
                                            title="Game 2",
                                            description="This is the second game.",
                                            author="anon2",
                                            file=SimpleUploadedFile(name="Game 2",content=b"a"*300)
                                                )

        cls.game1.buttons.create(chip8_key=0,button_id="dir_left")
        cls.game1.buttons.create(chip8_key=1,button_id="dir_right")
        cls.game1.keys.create(chip8_key=0,keyboard_code="F1")
        cls.game1.keys.create(chip8_key=1,keyboard_code="F2")


    def test_get_game_list(self):
        response = self.client.get(reverse("chip8:list_json"),format="json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data),2,msg=f"Returned {len(response.data)} results. 2 Expected")

        #test that response only includes id and title
        for game in response.data:
            self.assertEquals(len(game),2,msg=f"Game listing has {len(game)} attributes. Two expected.")

            self.assertTrue('id' in game.keys())
            self.assertTrue('title' in game.keys())


    def test_game_list_denied_methods(self):
        url = reverse("chip8:list_json")
        
        response = self.client.post(url,format='json')
        self.assertEquals(response.status_code,405)

        response = self.client.put(url,format='json')
        self.assertEquals(response.status_code,405)

        response = self.client.patch(url,format='json')
        self.assertEquals(response.status_code,405)

        response = self.client.delete(url,format='json')
        self.assertEquals(response.status_code,405)

    
    def test_get_game_config(self):
        id = self.game1.id

        response = self.client.get(reverse("chip8:game_json",args=[id]),format='json')

        self.assertEquals(response.status_code,200)
        response_length = len(response.data)
        self.assertEquals(response_length,7,msg=f"Game has {response_length} attributes. Expected 7.")
        
        game = response.data
        self.assertEquals(game['id'],self.game1.id)
        self.assertEquals(game['title'],self.game1.title)
        self.assertEquals(game['description'],self.game1.description)
        self.assertEquals(game['author'],self.game1.author)
        #test for gamefile url...note: testserver adds full url vs db, so test end of returned url
        game_file_url_end = game['file'][-1 * len(self.game1.file.url):]

        self.assertEquals(game_file_url_end,self.game1.file.url,msg=game['file'])
        buttons_length = len(game['buttons'])
        self.assertEquals(buttons_length,2,msg=f"Game has {buttons_length} buttons. Only 2 configured")
        keys_length = len(game['keys'])
        self.assertEquals(keys_length,2,msg=f"Game has {keys_length} keys. Only 2 configured.")


        #test configuration items
        for button in game['buttons']:
            button_attr_len = len(button)
            self.assertEquals(button_attr_len,3,msg=f"Button config has {button_attr_len} attributes. 3 expected.")
            self.assertTrue('id' in button.keys())
            self.assertTrue('button_id' in button.keys())
            self.assertTrue('chip8_key' in button.keys())


        for key in game['keys']:
            key_attr_length = len(key)
            self.assertEquals(key_attr_length,3,msg=f"Key config has {key_attr_length} attributes. 3 expected.")
            self.assertTrue('id' in key.keys())
            self.assertTrue('keyboard_code' in key.keys())
            self.assertTrue('chip8_key' in key.keys())

    def test_game_config_denied_methods(self):
        id = self.game1.id
        game_url = reverse("chip8:game_json",args=[id])
        self.assertEquals(self.client.post(game_url,format='json').status_code,405)
        self.assertEquals(self.client.put(game_url,format='json').status_code,405)
        self.assertEquals(self.client.patch(game_url,format='json').status_code,405)
        self.assertEquals(self.client.delete(game_url,format='json').status_code,405)


