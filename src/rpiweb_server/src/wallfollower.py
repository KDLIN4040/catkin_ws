import time
import Sensor as s
import Movement as mv
import RPi.GPIO as GPIO
import numpy as np
import threading 

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

class wallfollower(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
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
                        mv.stopmotors()
                        mv.goback()
                        time.sleep(0.5)
                        mv.turn_left()
                        time.sleep(0.3)
                    elif right < 20 :
                        mv.turn_left()
                        time.sleep(0.2)
                    elif left < 20 :
                        mv.turn_right()
                        time.sleep(0.2)
                    elif sweetspot_lowerbond < right1 < sweetspot_upperbond :
                        mv.goforward()
                        time.sleep(0.2)
                    else:
                        mv.move_arc()  
                    mv.goforward()
                    time.sleep(0.1)
                    time.sleep(0.01)

        except KeyboardInterrupt:
            GPIO.cleanup()
            time.sleep(1)
            print("stop")        

if __name__ == "__main__":
    threads = []
    t = wallfollower()
    t.start()
    time.sleep(1)
