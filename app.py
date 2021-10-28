#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import logging
import traceback
import time
import json
# import subprocess
from datetime import datetime, timedelta
import argparse
import picamera

log = logging.getLogger(__name__)


class Camera:
    def __init__(self, config):
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
        zoom = config['zoom']
        self.device.zoom = (0.0, 0.0, zoom, zoom)
        self.IsRecording = False


    # Capture a video according the recorder parameter
    def record(self, recorder):

        for i in range(0, recorder.samples):

            time.sleep(recorder.first_offset) if i == 0 else time.sleep(recorder.offset)

            sample = i + 1

            filename = time.strftime('%Y%m%d%H%M%S')

            now = datetime.now()
            delta = now + timedelta(seconds=recorder.duration)

            print("Recording sample {2} of {0} begining {1}".format(recorder.samples, now.strftime("%Y-%m-%d %H:%M:%S"), sample))
            self.IsRecording = True
            self.device.start_recording('%s.h264' % filename)
            self.device.wait_recording(recorder.duration)
            self.device.stop_recording()
            self.IsRecording = False
            print("Recording sample {2} of {0} complete {1}".format(recorder.samples, delta.strftime("%Y-%m-%d %H:%M:%S"), sample))


class Recorder:
    def __init__(self, app_config, rec_config):
        self.cycle = rec_config['cycle']
        self.duration = rec_config['duration']
        self.samples = rec_config['samples']

        # Number of seconds for the startup to synchronize with trafic light cycle
        self.start = self.duration / 2

        # First offset of the 1st video
        self.first_offset = self.cycle - self.start

        # Offset for the next X videos
        self.offset = self.cycle - self.duration

        self.camera = Camera(app_config)

    def stop(self):
        if self.camera.IsRecording:
            self.camera.device.stop_recording()
        self.camera.device.close()

    def record(self):
        self.camera.record(self)


def main(args=None):

    parser = argparse.ArgumentParser(description='trafic-light-recorder')

    parser.add_argument('-f', '--filename', dest='filename',
        required=True, help='JSON filename containing recording parameters')

    args = parser.parse_args(args if args is not None else sys.argv[1:])

    # Global config
    with open('global.json') as global_data:
        global_config = json.load(global_data)

    # Recording configuration
    with open(args.filename) as record_data:
        record_config = json.load(record_data)

    # The recorder - A Panasonic VHS 4-Head Hi-Fi Stereo
    recorder = Recorder(global_config, record_config)

    print("CTRL+C to exit")
    try:

        key = input("Press a key when the trafic light turn to GREEN # ")  # lint:ok
        recorder.record()

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
