'''
ESC204 2023S Lab 2 Task D
Task: Light up external LED on button press.
'''
# Import libraries needed for blinking the LED
import board
import digitalio
import time
import alarm
import pwmio
import analogio
from adafruit_debouncer import Debouncer

# Configure the internal GPIO connected to the LED as a digital output

#ledr = digitalio.DigitalInOut(board.GP6)
#ledr.direction = digitalio.Direction.OUTPUT

#ledg = digitalio.DigitalInOut(board.GP11)
#ledg.direction = digitalio.Direction.OUTPUT

#ledb = digitalio.DigitalInOut(board.GP7)
#ledb.direction = digitalio.Direction.OUTPUT

# Configure the internal GPIO connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up
switch = Debouncer(button)

pwmr = pwmio.PWMOut(board.GP6, frequency=5000, duty_cycle=0)
pwmg = pwmio.PWMOut(board.GP11, frequency=5000, duty_cycle=0)
pwmb = pwmio.PWMOut(board.GP7, frequency=5000, duty_cycle=0)



def mode_1():
	pwmr.duty_cycle = 0
	pwmg.duty_cycle = 0
	pwmb.duty_cycle = 0
	mode = 1
	return mode

def mode_2(raw):
	pwmr.duty_cycle = raw
	pwmg.duty_cycle = raw
	pwmb.duty_cycle = raw
	print(pwmr.duty_cycle)
	print(pwmg.duty_cycle)
	mode = 2
	return mode

def mode_3(raw, edge_count, time_start, cur_time, mode):
	if((time_start != 0) and (cur_time - time_start) > 5):
		time_start = 0
		edge_count = 1
		mode = mode_1()
	else:
		pwmr.duty_cycle = raw
		pwmg.duty_cycle = 0
		pwmb.duty_cycle = raw
		print(pwmr.duty_cycle)
		print(pwmg.duty_cycle)
		mode = 3
	return edge_count, mode

def change_led_brightness(raw, delay_start, knob, mode):
	if(delay_start == 0):
		delay_start = time.monotonic()
	elif(time.monotonic() - delay_start > 0.01):
		raw = knob.value
		delay_start = 0
	if(mode == 1):
		pwmr.duty_cycle = 0
		pwmg.duty_cycle = 0
		pwmb.duty_cycle = 0
	elif(mode == 2):
		pwmr.duty_cycle = raw
		pwmg.duty_cycle = raw
		pwmb.duty_cycle = raw
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
	knob = analogio.AnalogIn(board.GP26)
	raw = 60000
	mode = 1
	while True:
		switch.update()
		if(switch.fell):
			edge_count += 1
			cur_time = time.monotonic()
			if((edge_count % 3) == 1):
				time_start = 0
				mode = mode_1()
			elif((edge_count % 3) == 2):
				mode = mode_2(raw)
				time_start = time.monotonic()
			else:
				edge_count, mode = mode_3(raw, edge_count, time_start, cur_time, mode)
		raw, delay_start = change_led_brightness(raw, delay_start, knob, mode)






