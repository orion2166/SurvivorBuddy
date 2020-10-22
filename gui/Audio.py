#!/usr/bin/env python3
"""Pass input directly to output.
https://app.assembla.com/spaces/portaudio/git/source/master/test/patest_wire.c
"""
import argparse
import time
from threading import Thread
import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class Audio():
    
    def __init__(self):
        self.SAMPLERATE = 44100
        self.CHANNELS = 2 # python -m sounddevice
        #print (sd.query_devices())
        self.survivorSpeaker = -1
        self.survivorMic = -1
        self.responderSpeaker = -1
        self.responderMic = -1

    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def initializeStart(self):
        # parser = argparse.ArgumentParser(add_help=False)
        # parser.add_argument(
        #     '-l', '--list-devices', action='store_true',
        #     help='show list of audio devices and exit')
        # args, remaining = parser.parse_known_args()
        # if args.list_devices:
        #     print(sd.query_devices())
        #     parser.exit(0)
        # parser = argparse.ArgumentParser(
        #     description=__doc__,
        #     formatter_class=argparse.RawDescriptionHelpFormatter,
        #     parents=[parser])
        # parser.add_argument(
        #     '-i', '--input-device', type=int_or_str,
        #     help='input device (numeric ID or substring)')
        # parser.add_argument(
        #     '-o', '--output-device', type=int_or_str,
        #     help='output device (numeric ID or substring)')
        # parser.add_argument(
        #     '-c', '--channels', type=int, default=2,
        #     help='number of channels')
        # parser.add_argument('--dtype', help='audio data type')
        # parser.add_argument('--samplerate', type=float, help='sampling rate')
        # parser.add_argument('--blocksize', type=int, help='block size')
        # parser.add_argument('--latency', type=float, help='latency in seconds')
        # args = parser.parse_args(remaining)

        print('default.device='+str(sd.default.device))
        

        ##sd.default.device = sd.query_devices()
        


    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)
        outdata[:] = indata

    def createDeviceList(self):
        deviceList = sd.query_devices()
        newList = {}
        for index, i in enumerate(deviceList):
            #if (i['hostapi'] ==0):
            if (0 ==0):
                newList[i['name']] = index
        print(newList)
        return newList

    def setSurvivorSpeaker(self, survivorSpeaker):
        print("set survivorSpeaker with "+str(survivorSpeaker))
        self.survivorSpeaker = survivorSpeaker
        self.checkComsReady()

    def setSurvivorMic(self, survivorMic):
        print("set survivorMic with "+str(survivorMic))
        self.survivorMic = survivorMic
        self.checkComsReady()

    def setResponderSpeaker(self, responderSpeaker):
        print("set responderSpeaker with "+str(responderSpeaker))
        self.responderSpeaker = responderSpeaker
        self.checkComsReady()

    def setResponderMic(self, responderMic):
        print("set responderMic with "+str(responderMic))
        self.responderMic = responderMic
        self.checkComsReady()

    def checkComsReady(self):
        if (self.responderMic != -1 and self.responderSpeaker != -1 and self.survivorMic != -1 and self.survivorSpeaker != -1):
            self.startComs()

    def startComs(self):
        Thread(target = self.responderComs).start()
        Thread(target = self.survivorComs).start()

    def responderComs(self):
        print("responder coms started")
        sd.default.device = [self.responderMic,self.survivorSpeaker] #input/output   Microphone Array (Realtek High / Headphones (Realtek High Defin
        with sd.Stream(device=(sd.default.device),
                        samplerate=sd.default.samplerate, blocksize=sd.default.blocksize,
                        dtype=sd.default.dtype, latency=sd.default.latency,
                        channels=sd.default.channels, callback=self.callback):
                print('#' * 80)
                print('press Return to quit respondercoms')
                print('#' * 80)
                input()


    def survivorComs(self):
        print('#' * 80)
        print("survivor coms started")
        sd.default.device = [self.survivorMic,self.responderSpeaker] #input/output    Microphone (HD Pro Webcam C920)/Headset Earphone (Razer Audio C
        

        with sd.Stream(device=(sd.default.device),
                        samplerate=sd.default.samplerate, blocksize=sd.default.blocksize,
                        dtype=sd.default.dtype, latency=sd.default.latency,
                        channels=sd.default.channels, callback=self.callback):
                        
                print('#' * 80)
                print('press Return to quit survivorcoms')
                print('#' * 80)
                input()

# audio = Audio()
# audio.createDeviceList()
#audio.setDevices(10, 2, 6, 1)
#audio.startComs()