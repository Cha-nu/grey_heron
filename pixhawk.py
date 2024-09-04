from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import math
import argparse

#연결 시도
def connectMyCopter():
	vehicle = connect('/dev/ttyS0', baud=57600)
	print("version : %s" % vehicle.version)
	print("Attitude : %s" % vehicle.attitude)

	return vehicle

print("Hi")
vehicle = connectMyCopter()

#시동
def arm():
    print("try Arming")
    time.sleep(2)
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(2)
    vehicle.armed=True
    while vehicle.armed==False or not vehicle.mode.name == 'GUIDED':
        print("Waiting for drone to become armed...")
        time.sleep(1)
        vehicle.mode = VehicleMode("GUIDED")
        time.sleep(2)
        vehicle.armed=True
    print("Vehicle is now armed.")
    print("OMG props are spinning!!!")

    return None

# 이륙
def takeOff(TargetAltitude):
    print("Taking off")
    time.sleep(1)
    vehicle.simple_takeoff(TargetAltitude)
    while True:
        time.sleep(1)
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= TargetAltitude:
            print("reach")
            break
	
    return None
'''
def highjack():
    풍선을 추적하여 캐치하는 함수
'''
try:
    arm()
    takeOff()
    vehicle.airspeed = 5
    vehicle.groundspeed = 5

    print("return to launch")
    vehicle.mode = VehicleMode("RTL")

    print("vehicle close")
    vehicle.close()
except:
    print("return to launch")
    vehicle.mode = VehicleMode("RTL")

    print("vehicle close")
    vehicle.close()