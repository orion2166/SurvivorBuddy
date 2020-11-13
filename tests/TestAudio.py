import sys
sys.path.append('../gui')

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from Audio import Audio
import sounddevice as sd
import time

class TestAudio(unittest.TestCase):
    finishedResponder = False
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

    def test_responderSpeaker(self):
        print("\n---------------------")
        print("Test Connect Responder Speaker 2.6")
        speakerIndex = 1
        print("input speaker index: "+str(speakerIndex))
        audio = Audio()
        audio.setResponderSpeaker(speakerIndex)
        print("expected output: "+str(speakerIndex))
        print("real output: "+str(audio.responderSpeaker))
        self.assertEqual(speakerIndex, audio.responderSpeaker)
        success = speakerIndex == audio.responderSpeaker
        if (success):
            print("PASSED")
        else:
            print("FAILED")
        
    def test_responderMic(self):
        print("\n---------------------")
        print("Test Connect Responder Microphone 2.8")
        micIndex = 2
        print("input mic index: "+str(micIndex))
        audio = Audio()
        audio.setResponderMic(micIndex)
        print("expected output: "+str(micIndex))
        print("real output: "+str(audio.responderMic))
        self.assertEqual(micIndex, audio.responderMic)
        success = micIndex == audio.responderMic
        if (success):
            print("PASSED")
        else:
            print("FAILED")

    def test_survivorSpeaker(self):
        print("\n---------------------")
        print("Test Connect Survivor Speaker 2.2")
        speakerIndex = 3
        print("input speaker index: "+str(speakerIndex))
        audio = Audio()
        audio.setSurvivorSpeaker(speakerIndex)
        print("expected output: "+str(speakerIndex))
        print("real output: "+str(audio.survivorSpeaker))
        self.assertEqual(speakerIndex, audio.survivorSpeaker)
        success = speakerIndex == audio.survivorSpeaker
        if (success):
            print("PASSED")
        else:
            print("FAILED")
        
    def test_survivorMic(self):
        print("\n---------------------")
        print("Test Connect Survivor Microphone 2.4")
        micIndex = 4
        print("input mic index: "+str(micIndex))
        audio = Audio()
        audio.setSurvivorMic(micIndex)
        print("expected output: "+str(micIndex))
        print("real output: "+str(audio.survivorMic))
        self.assertEqual(micIndex, audio.survivorMic)
        success = (micIndex == audio.survivorMic)
        if (success):
            print("PASSED")
        else:
            print("FAILED")

    def test_Coms(self):
        print("\n---------------------")
        print("Process A/V Data 3.6")
        audio = Audio()
        sd.Stream = MagicMock(return_value=sd.Stream())
        audio.pauseUntilUserInput = MagicMock(return_value='\n')
        micResponderIndex = 1
        speakerSurvivorIndex = 3
        micSurvivorIndex = 1
        speakerResponderIndex = -1
        print("input responder mic index :"+str(micResponderIndex))
        print("input survivor speaker index:"+str(speakerSurvivorIndex))
        print("input survivor mic index:"+str(micSurvivorIndex))
        print("input responder speaker index:"+str(speakerSurvivorIndex))
        audio.setResponderMic(int(micResponderIndex))
        audio.setSurvivorSpeaker(int(speakerSurvivorIndex))
        audio.setSurvivorMic(int(micSurvivorIndex))
        audio.setResponderSpeaker(int(speakerResponderIndex))

        print("output expected call to sd.Stream:" + str(True))
        print("output real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
        self.assertTrue(sd.Stream.__call__)
        self.assertEqual(audio.responderMic, micResponderIndex)
        self.assertEqual(audio.survivorSpeaker, speakerSurvivorIndex)
        success = (None == self.assertTrue(sd.Stream.__call__)) and ( audio.survivorSpeaker == speakerSurvivorIndex) and (audio.responderMic == micResponderIndex) 
        if (success):
            print("PASSED")
        else:
            print("FAILED")

        print("\n---------------------")
        print("Play Audio on Responder's Speaker 3.8")
        print("input survivor mic index:"+str(micSurvivorIndex))
        print("input responder speaker index:"+str(speakerSurvivorIndex))
        print("output expected call to sd.Stream:" + str(True))
        print("output real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
        success = ( audio.survivorSpeaker == speakerSurvivorIndex) and (None == self.assertTrue(sd.Stream.__call__))
        if (success):
            print("PASSED")
        else:
            print("FAILED")

        print("\n---------------------")
        print("Encode Responder Audio 5.2")
        print("input survivor mic index:"+str(micSurvivorIndex))
        print("input responder speaker index:"+str(speakerSurvivorIndex))
        print("output expected call to sd.Stream:" + str(True))
        print("output real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
        success = (None == self.assertTrue(audio.responderComs.__call__)) and (None == self.assertTrue(sd.Stream.__call__))
        if (success):
            print("PASSED")
        else:
            print("FAILED")
        
        print("\n---------------------")
        print("Encode Survivor Audio 5.4")
        print("input responder mic index :"+str(micResponderIndex))
        print("input survivor speaker index:"+str(speakerSurvivorIndex))
        print("output expected call to sd.Stream:" + str(True))
        print("output real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
        success = (None == self.assertTrue(audio.checkSurvivorComsReady.__call__)) and (None == self.assertTrue(sd.Stream.__call__))
        if (success):
            print("PASSED")
        else:
            print("FAILED")

        print("\n---------------------")
        print("Play Live Audio On Survivor Speaker 6.2")
        print("input responder mic index :"+str(micResponderIndex))
        print("input survivor speaker index:"+str(speakerSurvivorIndex))
        print("output expected call to sd.Stream:" + str(True))
        print("output real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
        success = (None == self.assertTrue(sd.Stream.__call__)) and (None == self.assertTrue(audio.checkSurvivorComsReady.__call__))
        if (success):
            print("PASSED")
        else:
            print("FAILED")


    

        # print("\n---------------------")
        # print("test_SurvivorComs")
        # audio = Audio()
        # sd.Stream = MagicMock(return_value=sd.Stream())
        # audio.pauseUntilUserInput = MagicMock(return_value='\n')
        # micSurvivorIndex = 1
        # speakerResponderIndex = 3
        # print("input survivor mic:"+str(micSurvivorIndex))
        # print("input responder speaker:"+str(speakerResponderIndex))
        # audio.setSurvivorMic(int(micSurvivorIndex))
        # #audio.setResponderSpeaker(int(speakerResponderIndex))
        # print("expected call to sd.Stream:" + str(True))
        # print("real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
        # self.assertTrue(sd.Stream.__call__)
        # self.assertEqual(audio.survivorMic, micSurvivorIndex)


    # def test_SurvivorComs(self):
    #     print("\n---------------------")
    #     print("test_SurvivorComs")
    #     audio = Audio()
    #     sd.Stream = MagicMock(return_value=sd.Stream())
    #     audio.pauseUntilUserInput = MagicMock(return_value='\n')
    #     micSurvivorIndex = 1
    #     speakerResponderIndex = 3
    #     print("input survivor mic:"+str(micSurvivorIndex))
    #     print("input responder speaker:"+str(speakerResponderIndex))
    #     audio.setSurvivorMic(int(micSurvivorIndex))
    #     audio.setResponderSpeaker(int(speakerResponderIndex))
    #     print("expected call to sd.Stream:" + str(True))
    #     print("real call to sd.Stream:" + str(None == self.assertTrue(sd.Stream.__call__)))
    #     self.assertTrue(sd.Stream.__call__)
    #     self.assertEqual(audio.survivorMic, micSurvivorIndex)
    #     self.assertEqual(audio.responderSpeaker, speakerResponderIndex)


    def callback(self, indata, outdata, frames, time, status):
            if status:
                print(status, flush=True)
            outdata[:] = indata
    # @patch('Audio.checkSurvivorComsReady')
    # def test_responderComs(self, mock_checkSurvivorComsReady):
    #     #Audio.setResponderMic(0)
    #     audio = Audio()
    #     audio.setResponderSpeaker(1)
    #     audio.setSurvivorMic(2)
    #     #Audio.setSurvivorSpeaker(3)
    #     self.assertTrue(mock_checkSurvivorComsReady.called)

        # audio = Audio()
        # #audio.responderComs()
        # sd.Stream = MagicMock(return_value=sd.Stream(device=(sd.default.device),
        #                 samplerate=sd.default.samplerate, blocksize=sd.default.blocksize,
        #                 dtype=sd.default.dtype, latency=sd.default.latency,
        #                 channels=sd.default.channels, callback=self.callback))
        # self.assertFalse(audio.responderComs())

if __name__ == '__main__':
    unittest.main()