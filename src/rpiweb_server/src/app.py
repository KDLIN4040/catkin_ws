'''
  Raspberry Pi GPIO Status and Control
'''
from flask import Flask, render_template, request
import time
import Sensor as s
import RPi.GPIO as GPIO
import numpy as np
import threading 

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#define actuators motor GPIOs
right_motorEA_pin=12
right_motor_pin1 = 16
right_motor_pin2 = 18
left_motorEB_pin = 22
left_motor_pin1 = 32
left_motor_pin2 = 24

#initialize GPIO status variables
forwardSts = 0
movement = 0
forwardSts = 0
backwardSts = 0
turnrightSts = 0
turnleftSts = 0

#Define motor pins as output
GPIO.setup(right_motor_pin1,GPIO.OUT)
GPIO.setup(right_motor_pin2,GPIO.OUT)
GPIO.setup(right_motorEA_pin,GPIO.OUT)
r = GPIO.PWM(right_motorEA_pin,50) # GPIO for PWM with 50Hz
GPIO.setup(left_motor_pin1,GPIO.OUT)
GPIO.setup(left_motor_pin2,GPIO.OUT)
GPIO.setup(left_motorEB_pin,GPIO.OUT)
l = GPIO.PWM(left_motorEB_pin,50) # GPIO for PWM with 50Hz


#define car movement
def backward():
  GPIO.output(right_motor_pin1,1)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,1)
  GPIO.output(left_motor_pin2 ,0)
  r.start(100)
  l.start(100)

def forward():
  GPIO.output(right_motor_pin1,0)
  GPIO.output(right_motor_pin2,1)
  GPIO.output(left_motor_pin1 ,0)
  GPIO.output(left_motor_pin2, 1)
  r.start(100)
  l.start(100)


def turnright():
  GPIO.output(right_motor_pin1,0)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,1)
  GPIO.output(left_motor_pin2, 0)
  r.start(100)
  l.start(100)


def turnleft():
  GPIO.output(right_motor_pin1,1)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,0)
  GPIO.output(left_motor_pin2, 0)
  r.start(100)
  l.start(100)


def stopmotors():
  GPIO.output(right_motor_pin1, False)
  GPIO.output(right_motor_pin2, False)
  GPIO.output(left_motor_pin1, False)
  GPIO.output(left_motor_pin2, False)
  time.sleep(1)


sweetspot_upperbond = 50
sweetspot_lowerbond = 30

### get the obstacle distance 
# Define GPIO for ultrasonic Front
front1_trigger_pin = 31
front1_echo_pin = 33
GPIO.setup(front1_trigger_pin, GPIO.OUT)
GPIO.setup(front1_echo_pin, GPIO.IN)

# Define GPIO for ultrasonic Right
front2_trigger_pin = 35
front2_echo_pin = 37
GPIO.setup(front2_trigger_pin, GPIO.OUT)
GPIO.setup(front2_echo_pin, GPIO.IN)

# Define GPIO for ultrasonic Left
left_trigger_pin = 13 
left_echo_pin = 15
GPIO.setup(left_trigger_pin, GPIO.OUT)
GPIO.setup(left_echo_pin, GPIO.IN)

# Define GPIO for wallfollowing 
right_trigger_pin = 38 
right_echo_pin = 40
GPIO.setup(right_trigger_pin, GPIO.OUT)
GPIO.setup(right_echo_pin, GPIO.IN)

def right_distance():
    distance = s.get_distance(right_trigger_pin,right_echo_pin)
    return distance

def front1_distance():
    frontobstacle_distacne_cm = s.get_distance(front1_trigger_pin,front1_echo_pin)
    return(frontobstacle_distacne_cm)

def front2_distance():
    rightobstacle_distance_cm = s.get_distance(front2_trigger_pin,front2_echo_pin)
    return(rightobstacle_distance_cm)

def left_distance():
    leftobstacle_distance_cm  = s.get_distance(left_trigger_pin, left_echo_pin)
    return(leftobstacle_distance_cm )

autoflag = True

def wallfollower():
        try:    
            right1 = 40
            right2 = 40
            front1 = 40
            front2 = 40
            left   = 40
            while True:
                global autoflag
                if (autoflag == True):
                    right = right_distance()
                    front1 = front1_distance()
                    front2 = front2_distance()
                    left   = left_distance()           
                    print("right:{},front1:{},front2:{},left:{}".format(right,front1,front2,left))
                    
                    mv.goforward()
                    
                    if (front1 < 5) or (front2 < 5):
                        stopmotors()
                        backward()
                        time.sleep(0.5)
                        turnleft()
                        time.sleep(0.3)
                    elif right < 20 :
                        turnleft()
                        time.sleep(0.2)
                    elif left < 20 :
                        turnright()
                        time.sleep(0.2)
                    elif sweetspot_lowerbond < right < sweetspot_upperbond :
                        forward()
                        time.sleep(0.2)
                    else:
                        forward()  
                    forward()
                    time.sleep(0.01)

        except KeyboardInterrupt:
            GPIO.cleanup()
            time.sleep(1)
            print("stop") 

@app.route("/")
def index():
  global forwardSts
  global backwardSts
  global turnrightSts
  global turnleftSts
  templateData = {
              'title' : 'GPIO output Status!',
              'forward'  : forwardSts,
              'turnright'  : turnrightSts,
              'turnleft'  : turnleftSts,
              'backward'  : backwardSts,
        }
  return render_template('index.html', **templateData)
  
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
  global forwardSts
  global backwardSts
  global turnrightSts
  global turnleftSts
  global autoflag
  
  if deviceName == 'auto':
    movement = 'auto'
  elif deviceName == 'forward':
    movement = 'forward'
  elif deviceName == 'turnright':
    movement = 'turnright'
  elif deviceName == 'turnleft':
    movement = 'turnleft'
  elif deviceName == 'backward':
    movement = 'backward'
  elif deviceName == 'stopmotors':
    movement = 'stopmotors'

  if action == "on":
    if movement == "auto" :
      autoflag = True 
      wallfollower()       
    elif movement == "forward" :
      forward()
    elif movement == "turnright":
      turnright()
    elif movement == "turnleft":
      turnleft()
    elif movement == "backward":
      backward()
    elif movement == "stopmotors":
      stopmotors()

  if action == "off":
    if movement == "auto" :
      autoflag = False
    elif movement == "forward" :
      stopmotors()
    elif movement == "turnright":
      stopmotors()
    elif movement == "turnleft":
      stopmotors()
    elif movement == "backward":
      stopmotors()


  templateData = {
              'forward'  : forwardSts,
              'turnright'  : turnrightSts,
              'turnleft'  : turnleftSts,
              'backward'  : backwardSts,
  }
  return render_template('index.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=81, debug=True)
