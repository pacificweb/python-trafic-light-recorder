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

def main(args=None):

	parser = argparse.ArgumentParser(description='trafic-light-recorder')

	parser.add_argument('-c',  '--cycle', dest='cycle', required=True, type=int,
		help='Duration, in seconds, of a full trafic light cycle')

	parser.add_argument('-d',  '--duration', dest='duration', required=True, type=int,
		help='Duration, in seconds, of a recording for a cycle')

	parser.add_argument('-s',  '--samples', dest='samples', required=True, type=int,
		help='Number of desired videos')

	args = parser.parse_args(args if args is not None else sys.argv[1:])

	loop=args.cycle
	rectime=args.duration
	samples=args.samples

	# Number of seconds for the startup to synchronize with trafic light loop
	start=rectime/2

	try:

		print "Ctrl+c to exit"

		# Camera
		print "Warming up camera..."
		camera = picamera.PiCamera()
		time.sleep(2)
		camera.resolution = (640,480)
		camera.exposure_mode = "auto"
		camera.image_effect = "none"
		camera.exposure_compensation = 0
		camera.ISO = 0
		camera.brightness = 50
		camera.contrast = 0
		camera.framerate = 15

		var = raw_input("Press a key when the trafic light turn to GREEN # ")

		# Adjust for syncronization at startup for the first video
		time.sleep(loop-start)
		timestr = time.strftime('%Y%m%d%H%M%S') + '.h264'
      
		# Record Simulation
		#print('start_recording ' + time.strftime('%Y%m%d%H%M%S'))
		#time.sleep(rectime)
			
		# Live mode
		print('start_recording ' + timestr)
		camera.start_recording(timestr)

		print('wait_recording ' + str(rectime))
		camera.wait_recording(rectime)

		camera.stop_recording()
		print('stop_recording ' + time.strftime('%Y%m%d%H%M%S'))
			
		# Next videos
		for i in range(2, samples):

			print "Awaiting light timeout"
			time.sleep(loop-rectime)

			# Simulation
			#print('StartRecording ' + time.strftime('%Y%m%d%H%M%S'))
			#time.sleep(rectime)

			# PROD
			timestr = time.strftime("%Y%m%d%H%M%S") + '.h264'

			print('start_recording ' + timestr)
			camera.start_recording(timestr)

			print('wait_recording ' + str(rectime))
			camera.wait_recording(rectime)

			print('stop_recording ' + time.strftime('%Y%m%d%H%M%S'))
			camera.stop_recording()

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
