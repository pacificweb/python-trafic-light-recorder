#!/usr/bin/python

import sys
import logging
import os
import time
import subprocess
import picamera
from datetime import datetime

def main(args=None):

	#TODO ARGV 
	loop=69
	#loop=12
	rectime=6
	start=-(rectime/2)

	#try:

	print "Camlight 1.0 / Ctrl+c to exit"

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

	var = raw_input("Ready, press a key when light turn to GREEN # ")

	# Demarrage decalee par duree / 2 
	time.sleep(loop+start)
	timestr = time.strftime('%Y%m%d%H%M%S') + '.h264'
      
	# DEV
	#print('start_recording ' + time.strftime('%Y%m%d%H%M%S'))
	#time.sleep(rectime)
			
	# PROD
	print('start_recording ' + timestr)
	camera.start_recording(timestr)
	print('wait_recording ' + str(rectime))
	camera.wait_recording(rectime)
	camera.stop_recording()
	print('stop_recording ' + time.strftime('%Y%m%d%H%M%S'))
			
	# Loop ajustee
	min=10
	for i in range(2, min):

		# Timeout before recording
		print "Await timeout"
		time.sleep(loop-rectime)

		# DEV
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

	#except (KeyboardInterrupt):
	#	print('interrupt received')
	#except :
	#	print "Unexpected error:", sys.exc_info()[0]
	#finally:
	#	print('Exit finally')
	#	sys.exit()

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]) or 0)
