import unittest
import requests
from unittest.mock import patch
import main

class TestMenuCommand(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        main.documents.append({"type": "TEST", "number": "TEST", "name": "TEST"})
        main.directories.update({'TEST': ['TEST']})

    @patch('main.input', return_value = 'TEST')
    def test_search_person(self, mock_input):
        self.assertEqual(main.search_person(), "TEST")

    @patch('main.input', return_value = 'TEST')
    def test_search_shelf(self, mock_input):
        self.assertEqual(main.search_shelf(), "TEST")

    @patch('main.input', side_effect=['TEST1', 'TEST1', 'TEST1', 'TEST'])
    def test_new_document(self, mock_input):
        main.new_document()
        self.assertIn({"type": "TEST1", "number": "TEST1", "name": "TEST1"}, main.documents)
        self.assertIn("TEST1", main.directories['TEST'])
        main.documents.pop(-1)
        main.directories['TEST'] = ['TEST']

    @patch('main.input', return_value = 'TEST')
    def test_delete_document(self, mock_input):
        main.delete_document()
        self.assertNotIn({"type": "TEST", "number": "TEST", "name": "TEST"}, main.documents)
        self.assertNotIn("TEST", main.directories['TEST'])
        main.documents.append({"type": "TEST", "number": "TEST", "name": "TEST"})
        main.directories.update({'TEST': ['TEST']})

    @patch('main.input', side_effect=['TEST', 'TEST1'])
    def test_move_document(self, mock_input):
        main.directories.update({'TEST1': []})
        main.move_document()
        self.assertNotIn("TEST", main.directories['TEST'])
        self.assertIn("TEST", main.directories['TEST1'])
        main.directories.update({'TEST': ['TEST']})
        main.directories.pop('TEST1')

    @classmethod
    def tearDownClass(cls):
        main.documents.remove({"type": "TEST", "number": "TEST", "name": "TEST"})
        main.directories.pop('TEST')

class TestYandex(unittest.TestCase):
    token = ''
    def test_YaUploader_new_folder_1(self):
        #Проверка кода ответа
        uploader = main.YaUploader('TEST')
        result = uploader.new_folder()
        self.assertEqual("Папка на создана на Я.Диск", result)

    def test_YaUploader_new_folder_2(self):
        #Есть ли папка
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': "disk:/"}
        result = requests.get(url, headers=headers, params=params).json()
        dirs = []
        for item in result['_embedded']['items']:
            if item['type'] == 'dir':
                dirs.append(item['name'])
        self.assertIn("TEST", dirs, 'Папка не была создана')

    @classmethod
    def tearDownClass(cls):
        #Удаление тестовой папки
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': "disk:/TEST"}
        requests.delete(url, headers=headers, params=params)

if __name__ == '__main__':
  unittest.main()