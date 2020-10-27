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
        self.responderComsOn = False
        self.survivorComsOn = False
        self.stop_responderComs = False
        self.stop_survivorComs = False
        

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

        print('default.device='+str(sd.default.device), flush=True)
        

        ##sd.default.device = sd.query_devices()
        


    def callback(self, indata, outdata, frames, time, status):
        if status:
            print(status, flush=True)
        outdata[:] = indata

    def createOutputDeviceList(self):
        deviceList = sd.query_devices()
        newList = {}
        for index, i in enumerate(deviceList):
            if (i['max_input_channels'] ==0):
                newList[i['name']] = index
        print(newList)
        return newList

    def createInputDeviceList(self):
        deviceList = sd.query_devices()
        newList = {}
        for index, i in enumerate(deviceList):
            if (i['max_output_channels'] ==0):
                newList[i['name']] = index
        print(newList)
        return newList

    def setSurvivorSpeaker(self, survivorSpeaker):
        print("set survivorSpeaker with "+str(survivorSpeaker), flush=True)
        self.survivorSpeaker = survivorSpeaker
        self.checkResponderComsReady()

    def setSurvivorMic(self, survivorMic):
        print("set survivorMic with "+str(survivorMic), flush=True)
        self.survivorMic = survivorMic
        self.checkSurvivorComsReady()

    def setResponderSpeaker(self, responderSpeaker):
        print("set responderSpeaker with "+str(responderSpeaker), flush=True)
        self.responderSpeaker = responderSpeaker
        self.checkSurvivorComsReady()

    def setResponderMic(self, responderMic):
        print("set responderMic with "+str(responderMic), flush=True)
        self.responderMic = responderMic
        self.checkResponderComsReady()

    def checkResponderComsReady(self):
        if (self.responderMic != -1 and self.survivorSpeaker != -1 and not self.responderComsOn):
            self.responderComsOn = True
            Thread(target = self.responderComs).start()
        elif(self.responderComsOn):
            #global stop_responderComs
            self.stop_responderComs = True
            self.responderComsOn = False
            self.checkResponderComsReady()

    def checkSurvivorComsReady(self):
        if (self.survivorMic != -1 and self.responderSpeaker != -1 and not self.survivorComsOn):
            self.survivorComsOn = True
            Thread(target = self.survivorComs).start()
        elif(self.survivorComsOn):
            #global stop_survivorComs
            self.stop_survivorComs = True
            self.survivorComsOn = False
            self.checkSurvivorComsReady()
            

    def responderComs(self):
        self.stop_responderComs = False
        print("responder coms started", flush=True)
        sd.default.device = [self.responderMic,self.survivorSpeaker] #input/output   Microphone Array (Realtek High / Headphones (Realtek High Defin
        with sd.Stream(device=(sd.default.device),
                        samplerate=sd.default.samplerate, blocksize=sd.default.blocksize,
                        dtype=sd.default.dtype, latency=sd.default.latency,
                        channels=sd.default.channels, callback=self.callback):
                print('#' * 80, flush=True)
                while True:
                    #global stop_responderComs
                    if (self.stop_responderComs):
                        break
                print("responderComs Stopped", flush=True)
                # print('press Return to quit respondercoms')
                # print('#' * 80)
                # input()


    def survivorComs(self):
        self.stop_survivorComs = False
        print('#' * 80, flush=True)
        print("survivor coms started", flush=True)
        sd.default.device = [self.survivorMic,self.responderSpeaker] #input/output    Microphone (HD Pro Webcam C920)/Headset Earphone (Razer Audio C
        

        with sd.Stream(device=(sd.default.device),
                        samplerate=sd.default.samplerate, blocksize=sd.default.blocksize,
                        dtype=sd.default.dtype, latency=sd.default.latency,
                        channels=sd.default.channels, callback=self.callback):
                        
                print('#' * 80, flush=True)
                while True:
                    #global stop_survivorComs
                    if (self.stop_survivorComs):
                        break
                print("survivorComs Stopped", flush=True)
                # print('press Return to quit survivorcoms')
                # print('#' * 80)
                # input()

# audio = Audio()
# audio.createDeviceList()
#audio.setDevices(10, 2, 6, 1)
#audio.startComs()