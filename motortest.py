#!/usr/bin/python

import RPi.GPIO as GPIO

def motorControl():
	IN1_pin = 35
	IN2_pin = 36
	PWM_control_pin = 37

	GPIO.setup(IN1_pin,GPIO.OUT)
  	GPIO.setup(IN2_pin,GPIO.OUT)
  	PWM_handle = GPIO.PWM(PWM_control_pin, 50)
  	PWM_handle.start(10)

if __name__ == '__main__':
	try:
		motorControl()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nFinishing")

		PWM_handle.stop()
        GPIO.cleanup()

		sys.exit(0)