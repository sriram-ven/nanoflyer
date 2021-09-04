#!/usr/bin/python

import time
import zmq
import RPi.GPIO as GPIO

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

left_servo_pin = 32
right_servo_pin = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_servo_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(right_servo_pin, GPIO.OUT, initial=GPIO.HIGH)


left_handle = GPIO.PWM(left_servo_pin, 50)
left_handle.start(50)

right_handle = GPIO.PWM(right_servo_pin, 50)
right_handle.start(50)

def pitch_control():
	oldPitch = 0
	leftServoPWM = 50
	rightServoPWM = 50

	while True:

		currentPitch = socket.recv()
		print('pitch: ', currentPitch)

		if (pitch < 0):
			leftServoPWM -= 0.01
			rightServoPWM -= 0.01
		if (pitch > 0):
			leftServoPWM += 0.01
			rightServoPWM += 0.01

		left_handle.ChangeDutyCycle(leftServoPWM)
		right_handle.ChangeDutyCycle(rightServoPWM)
		oldPitch = currentPitch

		time.sleep(0.05)


if __name__ == '__main__':
	try:
		pitch_control()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nFinishing")
		
		left_handle.stop()
        right_handle.stop()
        GPIO.cleanup()

		sys.exit(0)