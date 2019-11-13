import RPi.GPIO as GPIO
import time

PIN_IN = 23
PIN_OUT = 21

cont_time = 0 # x10[msec]
wait_time = 0
click = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_OUT, GPIO.OUT)
GPIO.setup(PIN_IN, GPIO.IN)

while 1:
	if GPIO.input(23) == GPIO.HIGH:
		GPIO.output(21, GPIO.HIGH)
		if cont_time > 20:			#長押し対応
			print("< 1s")
		elif click == 1 and wait_time < 10:	#2連打以上
			print("2(or more) click")
		wait_time = 0
		cont_time += 1
	else:
		GPIO.output(21, GPIO.LOW)
		if wait_time > 10:
			click = 0
		else :
			if cont_time != 0:
				click = 1
		cont_time = 0
		wait_time += 1

	time.sleep(0.05)

GPIO.cleanup()

