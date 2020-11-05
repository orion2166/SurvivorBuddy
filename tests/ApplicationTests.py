import sys
sys.path.append('../gui')

import tkinter as tk
import unittest
from unittest.mock import Mock
from unittest.mock import patch
from Application import Application

class ApplicationMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_Application(self):
        root = tk.Tk()
        app = Application(master=root)
        Application.create_widgets.assert_called_once()
        #Application.create_widgets.create_menu.assert_called_once()
        #Application.create_widgets.update_image.assert_called()

if __name__ == '__main__':
    unittest.main()