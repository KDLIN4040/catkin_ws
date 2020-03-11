import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

#define GPIO For Driver motors Right
right_motorEA_pin = 12
right_motor_pin1 = 16
right_motor_pin2 = 18
GPIO.setup(right_motor_pin1,GPIO.OUT)
GPIO.setup(right_motor_pin2,GPIO.OUT)
GPIO.setup(right_motorEA_pin,GPIO.OUT)
r = GPIO.PWM(right_motorEA_pin,50) # GPIO for PWM with 50Hz

#define GPIO For Driver motors Left
left_motorEB_pin = 26
left_motor_pin1 = 32
left_motor_pin2 = 24
GPIO.setup(left_motor_pin1,GPIO.OUT)
GPIO.setup(left_motor_pin2,GPIO.OUT)
GPIO.setup(left_motorEB_pin,GPIO.OUT)
l = GPIO.PWM(left_motorEB_pin,50) # GPIO for PWM with 50Hz

# Functions for driving
def goback():
    GPIO.output(right_motor_pin1,1)
    GPIO.output(right_motor_pin2,0)
    GPIO.output(left_motor_pin1 ,1)
    GPIO.output(left_motor_pin2 ,0)
    r.start(100)
    l.start(100)
    print("goback")

def goforward():
    GPIO.output(right_motor_pin1,0)
    GPIO.output(right_motor_pin2,1)
    GPIO.output(left_motor_pin1 ,0)
    GPIO.output(left_motor_pin2, 1)
    r.start(100)
    l.start(100)
    print("goforward")

def turn_right():
    GPIO.output(right_motor_pin1,0)
    GPIO.output(right_motor_pin2,0)
    GPIO.output(left_motor_pin1 ,1)
    GPIO.output(left_motor_pin2, 0)
    r.start(100)
    l.start(100)
    print("turn_right")
def turn_left():
    GPIO.output(right_motor_pin1,1)
    GPIO.output(right_motor_pin2,0)
    GPIO.output(left_motor_pin1 ,0)
    GPIO.output(left_motor_pin2, 0)
    r.start(100)
    l.start(100)
    print("turn_left")
def move_arc():
    GPIO.output(right_motor_pin1,1)
    GPIO.output(right_motor_pin2,0)
    GPIO.output(left_motor_pin1 ,1)
    GPIO.output(left_motor_pin2 ,0)
    r.start(10)
    l.start(100)
    print("move_arc")
'''    
def turnright(value):
    goforward()
    setup.l.ChangeDutyCycle(value)
    setup.r.ChangeDutyCycle(0)
    time.sleep(0.3)
    print("turn_right")

def turnleft(value):
    goforward()
    setup.r.ChangeDutyCycle(value)
    setup.l.ChangeDutyCycle(0)
    time.sleep(0.3)
    print("turn_left")
'''

def stopmotors():
    GPIO.output(right_motor_pin1, False)
    GPIO.output(right_motor_pin2, False)
    GPIO.output(left_motor_pin1, False)
    GPIO.output(left_motor_pin2, False)
    time.sleep(1)
