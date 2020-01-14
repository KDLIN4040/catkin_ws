#!/usr/bin/env python
# license removed for brevity
import rospy
from sensor_msgs.msg import Imu
import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
import math


SETTINGS_FILE = "RTIMULib"

#  computeHeight() - the conversion uses the formula:
#
#  h = (T0 / L0) * ((p / P0)**(-(R* * L0) / (g0 * M)) - 1)
#
#  where:
#  h  = height above sea level
#  T0 = standard temperature at sea level = 288.15
#  L0 = standard temperatur elapse rate = -0.0065
#  p  = measured pressure
#  P0 = static pressure = 1013.25
#  g0 = gravitational acceleration = 9.80665
#  M  = mloecular mass of earth's air = 0.0289644
#  R* = universal gas constant = 8.31432
#
#  Given the constants, this works out to:
#
#  h = 44330.8 * (1 - (p / P0)**0.190263)

def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
    
print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

print("IMU Name: " + imu.IMUName())
print("Pressure Name: " + pressure.pressureName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded");

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

if (not pressure.pressureInit()):
    print("Pressure sensor Init Failed")
else:
    print("Pressure sensor Init Succeeded")

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)
pub = rospy.Publisher('imu', Imu, queue_size=1)
# Initialize the node and name it.
rospy.init_node('imu_publish')
rospy.loginfo('Starting ImuPublisherNode')
while True:
  
  if imu.IMURead():

    # x, y, z = imu.getFusionData()
    # print("%f %f %f" % (x,y,z))
    data = imu.getIMUData()
    (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
    fusionPose = data["fusionPose"]
    
    #ROS sensor_msgs/Imu Message
    fusionQPose = data["fusionQPose"]
    gyro = data["gyro"]
    accel = data["accel"]

    #print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
        #math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
    seq = 0
    imu_msg = Imu()
    imu_msg.linear_acceleration = accel
    imu_msg.angular_velocity = gyro
    imu_msg.orientation = fusionQPose
    imu_msg.header.stamp = rospy.Time.now()
    imu_msg.header.frame_id = imu
    imu_msg.header.seq = seq
    seq += 1
    pub.publish(imu_msg)
    #print(imu_msg)
    time.sleep(1/1000)

    if (data["pressureValid"]):
        print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["pressure"])))
    if (data["temperatureValid"]):
        print("Temperature: %f" % (data["temperature"]))
    time.sleep(poll_interval*1.0/1000.0)

