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


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-c', '--channels', type=int, default=2,
    help='number of channels')
parser.add_argument('--dtype', help='audio data type')
parser.add_argument('--samplerate', type=float, help='sampling rate')
parser.add_argument('--blocksize', type=int, help='block size')
parser.add_argument('--latency', type=float, help='latency in seconds')
args = parser.parse_args(remaining)


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata


print('default.device='+str(sd.default.device))
SAMPLERATE = 44100
CHANNEL1 = 2 # python -m sounddevice
CHANNEL2 = 61

##sd.default.device = sd.query_devices()
print (sd.query_devices())
survivorSpeaker = int(input("Survivor Speaker num:"))
survivorMic = int(input("Survivor Mic num:"))
responderSpeaker = int(input("Responder Speaker num:"))
responderMic = int(input("Responder Mic num:"))

def responderComs():
    print("responder coms started")
    sd.default.device = [responderMic,survivorSpeaker] #input/output   Microphone Array (Realtek High / Headphones (Realtek High Defin
    with sd.Stream(device=(sd.default.device),
                    samplerate=args.samplerate, blocksize=args.blocksize,
                    dtype=args.dtype, latency=args.latency,
                    channels=args.channels, callback=callback):
            print('#' * 80)
            print('press Return to quit respondercoms')
            print('#' * 80)
            input()
    # try:
    #     with sd.Stream(device=(sd.default.device),
    #                 samplerate=args.samplerate, blocksize=args.blocksize,
    #                 dtype=args.dtype, latency=args.latency,
    #                 channels=args.channels, callback=callback):
    #     # with sd.Stream(device=(args.input_device, args.output_device),
    #     #                samplerate=args.samplerate, blocksize=args.blocksize,
    #     #                dtype=args.dtype, latency=args.latency,
    #     #                channels=args.channels, callback=callback):
    #         print('#' * 80)
    #         #print('query'+str(OUTPUT_DEVICE) )
    #         print('press Return to quit respondercoms')
    #         print('#' * 80)
    #         input()
    # except KeyboardInterrupt:
    #     print('responder keybaord interrupt')
    #     parser.exit('')
    # except Exception as e:
    #     print('responder exception')
    #     parser.exit(type(e).__name__ + ': ' + str(e))

def survivorComs():
    print('#' * 80)
    print("survivor coms started")
    # print('survivorMic:'+str(sd.query_devices(survivorMic)))
    # print('responderSpeaker:'+str(sd.query_devices(responderSpeaker)))
    sd.default.device = [survivorMic,responderSpeaker] #input/output    Microphone (HD Pro Webcam C920)/Headset Earphone (Razer Audio C
    

    with sd.Stream(device=(sd.default.device),
                    samplerate=args.samplerate, blocksize=args.blocksize,
                    dtype=args.dtype, latency=args.latency,
                    channels=args.channels, callback=callback):
            print('#' * 80)
            print('press Return to quit survivorcoms')
            print('#' * 80)
            input()
    # try:
    #     with sd.Stream(device=(sd.default.device),
    #                 samplerate=args.samplerate, blocksize=args.blocksize,
    #                 dtype=args.dtype, latency=args.latency,
    #                 channels=args.channels, callback=callback):
    #     # with sd.Stream(device=(args.input_device, args.output_device),
    #     #                samplerate=args.samplerate, blocksize=args.blocksize,
    #     #                dtype=args.dtype, latency=args.latency,
    #     #                channels=args.channels, callback=callback):
    #         print('#' * 80)
    #         #print('query'+str(OUTPUT_DEVICE) )
    #         print('press Return to quit survivorcoms')
    #         print('#' * 80)
    #         input()
    # except KeyboardInterrupt:
    #     parser.exit('')
    # except Exception as e:

print(survivorMic)
Thread(target = responderComs).start()
Thread(target = survivorComs).start()
#responderComs()