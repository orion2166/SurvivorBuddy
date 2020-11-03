import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from Audio import Audio
import sounddevice as sd

class TestAudio(unittest.TestCase):
    
    def test_createOutputDeviceList(self):
        outputChannels = {'name' : "mic1", 'max_input_channels': 0, 'max_output_channels': 1}
        inputChannels = {'name' : "speaker1", 'max_input_channels': 1, 'max_output_channels': 0}
        deviceListMock = [outputChannels, inputChannels]
        deviceListExpected = {'mic1' : 0}
        audio = Audio()
        sd.query_devices = MagicMock(return_value=deviceListMock)
        self.assertEqual(audio.createOutputDeviceList(), deviceListExpected)

    def test_createInputDeviceList(self):
        outputChannels = {'name' : "mic1", 'max_input_channels': 0, 'max_output_channels': 1}
        inputChannels = {'name' : "speaker1", 'max_input_channels': 1, 'max_output_channels': 0}
        deviceListMock = [outputChannels, inputChannels]
        deviceListExpected = {'speaker1' : 1}
        audio = Audio()
        sd.query_devices = MagicMock(return_value=deviceListMock)
        self.assertEqual(audio.createInputDeviceList(), deviceListExpected)

    # def callback(self, indata, outdata, frames, time, status):
    #         if status:
    #             print(status, flush=True)
    #         outdata[:] = indata
    # @patch('Audio.input', return_value = 'test')
    # def test_responderComs(self, input):
    #     audio = Audio()
    #     #audio.responderComs()
    #     sd.Stream = MagicMock(return_value=sd.Stream(device=(sd.default.device),
    #                     samplerate=sd.default.samplerate, blocksize=sd.default.blocksize,
    #                     dtype=sd.default.dtype, latency=sd.default.latency,
    #                     channels=sd.default.channels, callback=self.callback))
    #     self.assertFalse(audio.responderComs())

if __name__ == '__main__':
    unittest.main()