#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import traceback
import time
# import subprocess
from datetime import datetime
import argparse
import picamera

log = logging.getLogger(__name__)


class Camera:
    def __init__(self):
        self.device = picamera.PiCamera()
        time.sleep(2)
        self.device.resolution = (640, 480)
        self.device.exposure_mode = "auto"
        self.device.image_effect = "none"
        self.device.exposure_compensation = 0
        self.device.ISO = 0
        self.device.brightness = 50
        self.device.contrast = 0
        self.device.framerate = 30  # Default
        self.IsRecording = False


    # Capture a video according the recorder parameter
    def record(self, recorder):

        for i in range(0, recorder.samples):

            time.sleep(recorder.first_offset) if i == 0 else time.sleep(recorder.offset)

            timestamp = time.strftime('%Y%m%d%H%M%S')

            print("Recording sample {2} of {0} begining {1}".format(recorder.samples, timestamp, i))
            self.IsRecording = True
            self.device.start_recording('%s.h264' % timestamp)
            self.device.wait_recording(recorder.duration)
            self.device.stop_recording()
            self.IsRecording = False
            print("Recording sample {2} of {0} complete {1}".format(recorder.samples, datetime.now(), i))


class Recorder:
    def __init__(self, cycle, duration, samples, json=None):
        self.cycle = cycle
        self.duration = duration
        self.samples = samples

        # Number of seconds for the startup to synchronize with trafic light cycle
        self.start = self.duration / 2

        self.first_offset = self.cycle - self.duration / 2
        self.offset = self.cycle - self.duration

        self.camera = Camera()

    def stop(self):
        if self.camera.IsRecording:
            self.camera.device.stop_recording()
        self.camera.device.close()

    def run(self):
        self.camera.record (self)


def main(args=None):

    # TODO Passer un fichier json de config au lieu d'une batche de parametre

    parser = argparse.ArgumentParser(description='trafic-light-recorder')

    parser.add_argument('-c', '--cycle', dest='cycle',
        required=True, type=int, help='Duration in seconds of light cycle')
    parser.add_argument('-d', '--duration', dest='duration',
        required=True, type=int, help='Duration in seconds of a recording for a cycle')
    parser.add_argument('-s', '--samples', dest='samples',
        required=True, type=int, help='Number of desired videos')

    args = parser.parse_args(args if args is not None else sys.argv[1:])

    config=None   # Futur
    recorder = Recorder(args.cycle, args.duration, args.samples, config)

    print("CTRL+C to exit")

    try:

        key = raw_input("Press a key when the trafic light turn to GREEN # ")  # lint:ok

        recorder.run()

    except (KeyboardInterrupt):
        print('interrupt received')
    except (NameError, TypeError, Exception):
        print(traceback.format_exc())
    finally:
        print('')
        recorder.stop()
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
