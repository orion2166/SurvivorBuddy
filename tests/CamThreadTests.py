import sys
sys.path.append('../gui')

import unittest
from unittest.mock import Mock
from CamThread import camPreview
from CamThread import camThread

class TestCamThreadMethods(unittest.TestCase):

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

    def test_camPreview(self):
        cam = Mock()
        test = camThread("Survivor Cam", 1, cam)
        test.camPreview = Mock()
        cam.read.assert_called_once()

if __name__ == '__main__':
    unittest.main()