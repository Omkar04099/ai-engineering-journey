import unittest
import os
import tempfile

class TestLifecyclePractice(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile(mode="w",delete=False) as file:
            self.temp_file_path = file.name

    def tearDown(self):
        os.remove(self.temp_file_path)

    def test_file_exists(self):
        isExists = os.path.exists(self.temp_file_path)
        self.assertTrue(isExists)

    def test_file_is_empty(self):
        with open(self.temp_file_path,"r") as file:
            content = file.read()
        self.assertEqual(content,"")

