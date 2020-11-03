import unittest
from unittest.mock import MagicMock
from Audio import Audio
import sounddevice as sd

class TestAudio(unittest.TestCase):
    
    def test_createOutputDeviceList(self):
        dictChannels = {'name' : "test", 'max_output_channels': 1, 'name2' : "test2", 'max_input_channels': 1}
        deviceListMock = [dictChannels]
        deviceListExpected = {'test' : 0}
        audio = Audio()
        #audio.createOutputDeviceList = MagicMock(return_value=listDevices)
        sd.query_devices = MagicMock(return_value=deviceListMock)
        self.assertEqual(audio.createOutputDeviceList(), deviceListExpected)

    def test_createInputDeviceList(self):
        dictChannels = {'name' : "test", 'max_output_channels': 1, 'name2' : "test2", 'max_input_channels': 1}
        deviceListMock = [dictChannels]
        deviceListExpected = {'test2' : 1}
        audio = Audio()
        #audio.createOutputDeviceList = MagicMock(return_value=listDevices)
        sd.query_devices = MagicMock(return_value=deviceListMock)
        self.assertEqual(audio.createInputDeviceList(), deviceListExpected)

    

if __name__ == '__main__':
    unittest.main()