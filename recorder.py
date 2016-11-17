#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import logging
import os
import time
import subprocess
import picamera
from datetime import datetime

def main(args=None):

	#TODO ARGV 
	loop=69					# Number of seconds for a complete Green to Gree cycle
	rectime=6				# Number of seconds of recording
	samples=10				# Number of video to capture

	# Local variables
	start=rectime/2			# Number of seconds for the startup before synchronize with loop

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
