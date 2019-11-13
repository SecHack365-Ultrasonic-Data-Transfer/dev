import RPi.GPIO as GPIO
import time

PIN_IN = 23
PIN_OUT = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_OUT, GPIO.OUT)
GPIO.setup(PIN_IN, GPIO.IN)

while 1:
	if GPIO.input(23) == GPIO.HIGH:
		GPIO.output(21, GPIO.HIGH)
	else:
		GPIO.output(21, GPIO.LOW)
	time.sleep(0.01)

GPIO.cleanup()

