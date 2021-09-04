#!/usr/bin/python

import qwiic_icm20948
import time
import sys
import math
import zmq

def pitch_estimate():

	GYRO_SENS = 65.536
	dT = 0.03
	pitch = 0
	roll = 0

	IMU = qwiic_icm20948.QwiicIcm20948()

	if IMU.connected == False:
		print('imu not connected')
		return
	IMU.begin()

	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5555")

	while True:
		if IMU.dataReady():
			IMU.getAgmt()

			pitch += (IMU.gxRaw/GYRO_SENS) * dT
			# roll -= (IMU.gyRaw/GYRO_SENS) * dT

			totalForce = math.hypot(IMU.axRaw, IMU.ayRAW, IMU.azRAW)
			if 0.9 < totalForce < 1.1:
				pitch = pitch * 0.98 + math.atan2(IMU.ayRaw, math.hypot(IMU.axRAW, IMU.azRAW)) * 180/math.pi * 0.02
				# roll = roll * 0.98 + math.atan2(-IMU.axRaw, IMU.azRAW) * 180/math.pi * 0.02

				p = (pitch * 180/math.pi)
				# r = (roll * 180/math.pi)
				print('pitch = ', p)
				socket.send(p)

			time.sleep(0.03)
		else:
			time.sleep(0.5)

if __name__ == '__main__':
	try:
		pitch_estimate()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nFinishing")
		sys.exit(0)