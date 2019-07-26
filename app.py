#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import traceback
import time
#import subprocess
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
        #self.device.framerate = 60

        self.IsRecording = False

    # Capture a video according the recorder parameter
    def capture(self, recorder):
        for i in range(0, recorder.samples):
            if i == 0:
                # First take
                time.sleep(recorder.first_offset)
            else:
                time.sleep(recorder.offset)
            filename = time.strftime('%Y%m%d%H%M%S')
            print("Recording sample {2} of {0} begining {1}".format(recorder.samples, datetime.now(), i))
            self.IsRecording = True
            self.device.start_recording('%s.h264' % filename)
            self.device.wait_recording(recorder.duration)
            self.device.stop_recording()
            self.IsRecording = False
            print("Recording sample {2} of {0} complete {1}".format(recorder.samples, datetime.now(), i))



class Recorder:
    def __init__(self, cycle, duration, samples):
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
        self.camera.capture(self)


def main(args=None):

    parser = argparse.ArgumentParser(description='trafic-light-recorder')

    parser.add_argument('-c', '--cycle', dest='cycle',
        required=True, type=int, help='Duration in seconds of light cycle')
    parser.add_argument('-d', '--duration', dest='duration',
        required=True, type=int, help='Duration in seconds of a recording for a cycle')
    parser.add_argument('-s', '--samples', dest='samples',
        required=True, type=int, help='Number of desired videos')

    args = parser.parse_args(args if args is not None else sys.argv[1:])

    recorder = Recorder(args.cycle, args.duration, args.samples)

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
