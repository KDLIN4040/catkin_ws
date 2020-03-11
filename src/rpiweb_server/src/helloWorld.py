
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
ledRed = 31
ledRedSts = 0
GPIO.setup(ledRed, GPIO.OUT)
GPIO.output(ledRed, GPIO.LOW)
@app.route('/')
def index():
    return 'Hello world'
    ledRedSts = GPIO.input(ledRed)
    templateData = {
                 'title' : 'GPIO output Status',
                 'ledRed': ledRedSts,
                   }
    return render_template('index.html',**templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
  if deviceName == 'ledRed':
     actuator = ledRed
  if action == "on":
     GPIO.output(actuator, GPIO.HIGH)
  if action == "off":
     GPIO.output(actuator, GPIO.LOW)

  ledRedSts = GPIO.input(ledRed)
  templateData = {
               'ledRed' : ledRedSts,
                 }
  return render_template('index.html',**templateData)
if __name__ == '__main__':
    app.run(debug=True, port=81, host='192.168.11.48')
