'''
ESC204 2023S Lab 2 Task D
Task: Light up external LED on button press.
'''

import board # Access to pins on the RP2040
import digitalio # GPIO input for the button
import time # For delays
import pwmio # PWM for LED brightness and the buzzer
import analogio # ADC input, used to control LED brightness
from adafruit_debouncer import Debouncer # Debouncer library, also for the button. For more information on dependency requirements see https://docs.circuitpython.org/projects/debouncer/en/stable/

# Configure the button input with a debouncer
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up
switch = Debouncer(button)

# Configure the LED outputs with PWM
pwmr = pwmio.PWMOut(board.GP6, frequency=5000, duty_cycle=0)
pwmg = pwmio.PWMOut(board.GP11, frequency=5000, duty_cycle=0)
pwmb = pwmio.PWMOut(board.GP7, frequency=5000, duty_cycle=0)

# Configure the buzzer output with PWM
buzzer = pwmio.PWMOut(board.GP16, variable_frequency = True)

# Configure the ADC (potentiometer knob) input
knob = analogio.AnalogIn(board.GP26)

def buzz(mode):
	if(mode == 1):
		buzzer.frequency = 440
	elif(mode == 2):
		buzzer.frequency = 392
	else:
		buzzer.frequency = 494
	buzzer.duty_cycle = 2**15
	time.sleep(0.1)
	buzzer.duty_cycle = 0

def mode_1():
	mode = 1
	buzz(mode)
	return mode

def mode_2():
	mode = 2
	buzz(mode)
	return mode

def mode_3(edge_count, time_start, cur_time, mode):
	if((time_start != 0) and (cur_time - time_start) > 5):
		time_start = 0
		edge_count = 1
		mode = mode_1()
	else:
		mode = 3
		buzz(mode)
	return edge_count, mode

def change_led_brightness(raw, delay_start, knob, mode):
	if(delay_start == 0):
		delay_start = time.monotonic()
	elif(time.monotonic() - delay_start > 0.01):
		raw = knob.value
		delay_start = 0
	print(raw)
	if(mode == 1):
		pwmr.duty_cycle = 0
		pwmg.duty_cycle = 0
		pwmb.duty_cycle = 0
	elif(mode == 2):
		if(raw < 1000):
			pwmr.duty_cycle = 0
			pwmg.duty_cycle = 0
			pwmb.duty_cycle = 0
		else:
			pwmr.duty_cycle = raw
			pwmg.duty_cycle = raw
			pwmb.duty_cycle = raw
	else:
		if(raw < 1000):
			pwmr.duty_cycle = 0
			pwmg.duty_cycle = 0
			pwmb.duty_cycle = 0
		else:
			pwmr.duty_cycle = raw
			pwmg.duty_cycle = 0
			pwmb.duty_cycle = raw
	return raw, delay_start

# Loop so the code runs continuously
if __name__ == "__main__":
	edge_count = 1
	time_start = 0
	cur_time = 0
	delay_start = 0
	raw = 60000
	mode = 1
	while True:
		switch.update()
		if(switch.fell):
			edge_count += 1
			cur_time = time.monotonic()
			if((edge_count % 3) == 1):
				mode = mode_1()
			elif((edge_count % 3) == 2):
				mode = mode_2()
				time_start = time.monotonic()
			else:
				edge_count, mode = mode_3(edge_count, time_start, cur_time, mode)
		raw, delay_start = change_led_brightness(raw, delay_start, knob, mode)








