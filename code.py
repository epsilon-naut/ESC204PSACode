'''
ESC204 2023S Lab 2 Task D
Task: Light up external LED on button press.
'''
# Import libraries needed for blinking the LED
import board
import digitalio
import asyncio
import countio
import time
import alarm

# Configure the internal GPIO connected to the LED as a digital output
ledb = digitalio.DigitalInOut(board.GP7)
ledb.direction = digitalio.Direction.OUTPUT

ledg = digitalio.DigitalInOut(board.GP11)
ledg.direction = digitalio.Direction.OUTPUT

ledr = digitalio.DigitalInOut(board.GP6)
ledr.direction = digitalio.Direction.OUTPUT

# Configure the internal GPIO connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN # Set the internal resistor to pull-up

def mode_1():
	ledr.value = True
	ledg.value = True
	ledb.value = False

def mode_2():
	ledr.value = True
	ledg.value = True
	ledb.value = True

def mode_3(edge_count):
	if((time_start != 0) and (cur_time - time_start) > 10):
		time_start = 0
		edge_count = 1
		mode_1()
	else:
		ledr.value = False
		ledg.value = False
		ledb.value = False
	return edge_count

edge_count = 0

time_start = 0

cur_time = 0

# Loop so the code runs continuously
if __name__ == "__main__":
	while True:
		while(button.value):
			pass
		while(not button.value):
			pass
		edge_count += 1
		print(edge_count)
		cur_time = time.monotonic()
		if((edge_count % 3) == 1):
			time_start = 0
			mode_1()
		elif((edge_count % 3) == 2):
			mode_2()
			time_start = time.monotonic()
		else:
			edge_count = mode_3(edge_count)
		time.sleep(0.1)
