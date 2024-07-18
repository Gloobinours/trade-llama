import unittest
from src import main

class TestMainMethod(unittest.TestCase):
    def test_main(self):
        actual: int = 3 
        truc: int = main.unpetittest()
        self.assertEqual(actual, truc)
    