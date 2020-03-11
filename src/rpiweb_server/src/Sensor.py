import RPi.GPIO as GPIO
import time
#Functions for Ultrasonic sensor    
def send_trigger_pulse(pin):
    GPIO.output(pin, True)
    time.sleep(0.02)
    GPIO.output(pin, False)

def wait_for_echo(echo_pin,value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count = count - 1

def get_distance(trigger,echo):
    send_trigger_pulse(trigger)
    wait_for_echo(echo,True, 5000)
    start = time.time()
    wait_for_echo(echo,False, 5000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 *100 /2
    return (distance_cm)