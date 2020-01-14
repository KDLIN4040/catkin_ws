'''
  Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#define actuators motor GPIOs
right_motorEA_pin=12
right_motor_pin1 = 16
right_motor_pin2 = 18
left_motorEB_pin = 26
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
def forward():
  GPIO.output(right_motor_pin1,1)
  GPIO.output(right_motor_pin2,0)
  GPIO.output(left_motor_pin1 ,1)
  GPIO.output(left_motor_pin2 ,0)
  r.start(100)
  l.start(100)

def backward():
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
  global movement
  global forwardSts
  global backwardSts
  global turnrightSts
  global turnleftSts

  if deviceName == 'forward':
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
    if movement == "forward" :
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
    if movement == "forward" :
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