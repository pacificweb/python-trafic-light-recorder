# python-trafic-light-recorder
- A python script to record a trafic light for a specific duration and a specific cycle in seconds
- The purpose of the script is to record vehicles burning red light
- Work with Raspberry-Pi / the camera module and the PiCamera Object Model
- You have to know the trafic light full cycle duration in seconds
- You have to start the script when the light turn to green
- You have to set a recording duration (Example 10 seconds)
- The script will record 5 seconds before turn to green and 5 seconds after turning to green.

# TODO 
- Move the code in main body in a kind of recorder class (rec = new Recorder(cycle, duration, samples)
- Pass in ARGS : trafic light cycle time, recording time for a cycle, number of videos to records
- A demo on Youtube
