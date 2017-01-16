#!/usr/bin/python -p
# Stream input audio to FM radio
import sys
import os
import subprocess

streaming_radio_process = None
streaming_microphone_process = None
streaming_speaker_process = None

fm_pipe_r, fm_pipe_w = os.pipe()

# Settings
frequency = 88.1
format = "S16_LE"
rate = 44100
channels = 2
input_device_name = "plughw:1,0"
debug = False


def main():
    # daemonize()
    stream_microphone()
    stream_output()
    return 0


def daemonize():
    fpid = os.fork()
    if fpid != 0:
        sys.exit(0)


def stream_microphone():
    global streaming_microphone_process

    # Record microphone
    streaming_microphone_process = subprocess.Popen(["arecord", "--format", format, "--rate", str(rate), "--device", input_device_name, "--channels", str(channels), "-"],
                                                    stdout=fm_pipe_w)
    print("Recording microphone")

def stream_output():
    if debug:
        stream_speaker()
    else:
        stream_radio()


def stream_speaker():
    global streaming_speaker_process

    # Play on speaker
    streaming_speaker_process = subprocess.Popen(["aplay", "--format", format, "--channels", str(channels), "--rate", str(rate)],
                                                 stdin=fm_pipe_r)
    print("Streaming to speakers")


def stream_radio():
    global streaming_radio_process

    # Broadcast on air
    streaming_radio_process = subprocess.Popen([os.path.join(os.path.dirname(os.path.abspath(__file__)), "pifm"),
                                                "-", str(frequency), str(rate), "stereo" if channels == 2 else "mono"],
                                               stdin=fm_pipe_r)
    print("Streaming to radio")


main()
