#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import os
import time
import subprocess
from datetime import datetime
import argparse
import picamera

log = logging.getLogger(__name__)

class Camera:

    def __init__(self):
        self.device = picamera.PiCamera()
        time.sleep(2)
        self.device.resolution = (640,480)
        self.device.exposure_mode = "auto"
        self.device.image_effect = "none"
        self.device.exposure_compensation = 0
        self.device.ISO = 0
        self.device.brightness = 50
        self.device.contrast = 0
        self.device.framerate = 15

    def capture(self, duration):
        timestr = time.strftime('%Y%m%d%H%M%S') + '.h264'
        self.device.start_recording(timestr)
        self.device.wait_recording(duration)
        self.device.stop_recording()


class Recorder:

    def __init__(self, cycle, duration, samples):
        self.cycle = cycle
        self.duration = duration
        self.samples = samples

        # Number of seconds for the startup to synchronize with trafic light cycle
        self.start = self.duration/2

        self.first_offset = self.cycle - self.duration / 2
        self.offset = self.cycle - self.duration

        self.cam = Camera()

    def stop(self):
        self.cam.device.close()

    def start(self):

        # First take
        time.sleep(self.first_offset)
        self.cam.capture(self.duration)

        # Next takes
        for i in range(2, self.samples):

            print ("Awaiting light timeout")
            time.sleep(self.offset)
            self.cam.capture(self.duration)

def main(args=None):

    parser = argparse.ArgumentParser(description='trafic-light-recorder')

    parser.add_argument('-c',  '--cycle', dest='cycle', required=True, type=int, help='Duration in seconds of light cycle')
    parser.add_argument('-d',  '--duration', dest='duration', required=True, type=int, help='Duration in seconds of a recording for a cycle')
    parser.add_argument('-s',  '--samples', dest='samples', required=True, type=int, help='Number of desired videos')

    args = parser.parse_args(args if args is not None else sys.argv[1:])

    recorder = Recorder(args.cycle, args.duration, args.samples)

    print("CTRL+C to exit")

    try:

        var = raw_input("Press a key when the trafic light turn to GREEN # ")

        recorder.run()

    except (KeyboardInterrupt):
        print('interrupt received')
    except NameError, e:
        print "NameError error:", e
    except Exception, e: # catch *all* exceptions 
        print "Unexpected error:", e
    finally:
        print('')
        sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
