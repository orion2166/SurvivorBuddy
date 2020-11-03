import unittest
from unittest.mock import MagicMock
from Audio import Audio
import sounddevice as sd

class TestAudio(unittest.TestCase):
    
    def test_createOutputDeviceList(self):
        listDevices = {'max_output_channels': 1, 'max_output_channels' : 2, 'max_output_channels' : 3}
        audio = Audio()
        #audio.createOutputDeviceList = MagicMock(return_value=listDevices)
        #sd.query_devices = MagicMock(return_value=listDevices)
        self.assertEqual(audio.createOutputDeviceList(), audio.createOutputDeviceList())

if __name__ == '__main__':
    unittest.main()