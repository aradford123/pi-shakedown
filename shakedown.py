#!/usr/bin/env python
import sys, os
from webexteamssdk import WebexTeamsAPI
import picamera
import time
import subprocess
from argparse import ArgumentParser
from servo import Servo
from Motor import Motor

from webex_config  import AUTH, ROOMID

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

def take_photo(message):
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        camera.start_preview()
        camera.annotate_text = message
        time.sleep(2)
        # Take a picture including the annotation
        camera.capture('img.jpg')

def take_video():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_recording('car_video.h264')
        camera.wait_recording(1)
        camera.stop_recording()

    # convert to mp4
    command = "MP4Box -add car_video.h264 car_video.mp4"
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

def main(dopost):
    print("Posting to webex teams" if dopost else "Testing mode, will not post to webex teams, use --post to post to teams")

    if "CHANGE" in AUTH:
        print("Please update webex Token in webex_config.py")
        sys.exit(1)    
    if "CHANGE" in ROOMID:
        print("Please update webex ROOMID in webex_config.py")
        sys.exit(1)    

    api = WebexTeamsAPI(access_token=AUTH)
    
    serial = getserial()
    pwm=Servo()
    pwm.setServoPwm('0',90)
    take_photo(serial)
    if dopost:
        api.messages.create(ROOMID, text="serial: {} @ 90".format(serial),
                        files=["img.jpg"])
    
    
    pwm.setServoPwm('0',45)
    take_photo(serial)
    if dopost:
        api.messages.create(ROOMID, text="serial: {} @ 45".format(serial),
                        files=["img.jpg"])

    pwm.setServoPwm('0',90)

    # move car for 1 second while taking a video
    PWM=Motor()
    PWM.setMotorModel(2000,2000,2000,2000)      
    take_video()

    # stop the car, sometimes fails
    for i in range(10):
        try: 
            PWM.setMotorModel(0,0,0,0)      
            print("Car stopped, attempt {}".format(i))
            break
        except OSError:
            print("Stop attempt #{} failed, retrying".format(i))
            time.sleep(.2)

    if dopost:
        api.messages.create(ROOMID, text="serial: {} video - mp4".format(serial),
                        files=["car_video.mp4"])

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--post', action="store_true", help="post to webex teams")
    args = parser.parse_args()
    main(args.post)
