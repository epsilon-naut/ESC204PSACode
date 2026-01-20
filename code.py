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

def mode_3():
	ledr.value = False
	ledg.value = False
	ledb.value = False

count = 0

async def button_pressed(pin):
	with countio.Counter(pin) as interrupt:
		while True:
			if interrupt.count > 1:
				interrupt.count = 0
				count += 1
				if(count % 3 == 1):
					mode_1()
				elif(count % 3 == 2):
					mode_2()
				else:
					mode_3()
			await asyncio.sleep(0)

async def main():
	button_wait = asyncio.create_task(button_pressed(button))
	await asyncio.gather(button_wait)

asyncio.run(main)
