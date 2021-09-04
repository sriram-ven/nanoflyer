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
	K_p, K_i, K_d = 1, 0, 0
	oldPitch = 0
	accumulator = 0
	leftServoPWM = 50
	rightServoPWM = 50

	while True:

		currentPitch = socket.recv()
		print('pitch: ', currentPitch)

		accumulator += currentPitch
		leftServoPWM = K_p * currentPitch + K_i * accumulator + K_d * - (currentPitch - oldPitch)
		rightServoPWM = K_p * currentPitch + K_i * accumulator + K_d * - (currentPitch - oldPitch)

		if leftServoPWM > 100:
			leftServoPWM = 100
			accumulator -= currentPitch
		if leftServoPWM < 0:
			leftServoPWM = 0
			accumulator -= currentPitch

		# lame (but probably better) approach 
		# if (currentPitch < 0):
		# 	leftServoPWM -= 0.01
		# 	rightServoPWM -= 0.01
		# if (currentPitch > 0):
		# 	leftServoPWM += 0.01
		# 	rightServoPWM += 0.01

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