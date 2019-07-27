# python-trafic-light-recorder
- A python script to record a trafic light for a specific duration and a specific cycle in seconds
- The purpose of the script is to record vehicles burning red light
- Works with Raspberry Pi, its camera module and the PiCamera Object Model
- Works only with a static light cycle 
- You have to calculate the green cycle in seconds
- You have to start the script when the light turn to green
- You have to set a recording duration 
- For example 10 seconds, the script will record 5 seconds before turning to green and 5 seconds after turning to green.
- Since it HD, convert with MP4Box -fps 30 -add source.h264 target.mp4 will rendre a flawless video
