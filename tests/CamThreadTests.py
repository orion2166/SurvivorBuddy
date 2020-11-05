import sys
sys.path.append('../gui')

import unittest
from unittest.mock import Mock
from CamThread import camPreview
from CamThread import camThread

class TestCamThreadMethods(unittest.TestCase):
    def test_camPreview(self):
        cam = Mock()
        test = camThread("Survivor Cam", 1, cam)
        test.camPreview = Mock()
        cam.read.assert_called_once()

if __name__ == '__main__':
    unittest.main()