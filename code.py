'''
Software for group PRA-0109-07's prototype for the ESC204 Winter 2026 PSA. 

The software supports only three states, an 'OFF' state with all LEDs turned off, a 
'HUMANS AND PLANTS' state with all LEDs turned on, and a 'PLANTS ONLY' state with the
green LED turned off. It is possible to cycle between all three states by pressing the 
button. The board starts in the 'OFF' state, but pressing the button repeatedly
causes it to cycle from 'OFF' to 'HUMANS AND PLANTS' to 'PLANTS ONLY', and eventually
cycling back to the 'OFF' state. This process can be repeated indefinitely, and each button
press advances the state of the prototype by one. 

For each state, the buzzer will play a distinct
corresponding note for 100 milliseconds, so those with visual impairment can also 
operate the device. 

Another key feature is a time- and state-dependent control loop design. When the prototype
has remained in the 'HUMANS AND PLANTS' state for more than 5 seconds, the next button press
will return the prototype to the 'OFF' state instead of progressing to the 'PLANTS ONLY'
state first. This provides the operator more comfort, as they can reach the 'OFF' state from 
the 'HUMANS AND PLANTS' state without having to reach the uncomfortable 'PLANTS ONLY' state
first. 

The final feature is an implementation of PWM (pulse width modulation) to control the 
brightness of the LEDs. The magnitude of this PWM output is directly connected to the 
magnitude of the ADC (analog to digital converter) input connected to a potentiometer on the 
prototype, allowing users to control the brightness of the LEDs using the potentiometer knob.
A lower cutoff limit exists to ensure the LED brightness can be set to zero if the knob is 
turned fully.  

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
pwm_red = pwmio.PWMOut(board.GP6, frequency=5000, duty_cycle=0)
pwm_green = pwmio.PWMOut(board.GP11, frequency=5000, duty_cycle=0)
pwm_blue = pwmio.PWMOut(board.GP7, frequency=5000, duty_cycle=0)

# Configure the buzzer output with PWM
buzzer = pwmio.PWMOut(board.GP16, variable_frequency = True)

# Configure the ADC (potentiometer knob) input
knob = analogio.AnalogIn(board.GP26)

# Code for the buzzer sound output. The buzzer will sound different notes depending on the 
# state of the prototype, represented by the variable 'state'.
def buzz(state):
	
	if(state == 1):
		buzzer.frequency = 440 # Frequency corresponds to the note A4
	elif(state == 2):
		buzzer.frequency = 392 # Frequency corresponds to the note G4
	else:
		buzzer.frequency = 494 # Frequency corresponds to the note B4
	
	buzzer.duty_cycle = 2**15 
	# The PWM is a 16-bit PWM output, meaning that for a given PWM cycle, there are 2**16
	# equal subdivisions of time where the state can either be HIGH or LOW. 
	# A sound wave spends half of their period above equilibrium ('HIGH') and 
	# half of their period below equilibrium ('LOW'), we replicate this by setting 
	# the duty cycle to exactly half HIGH and half LOW, which corresponds to a duty cycle 
	# (number of subdivisions spent HIGH) of 2**15.
	
	time.sleep(0.1) # Buzz the sound for 100 milliseconds

	buzzer.duty_cycle = 0 # Turn the buzzer off by setting a PWM duty cycle of 0

# Code for the 'OFF' state.
def off(): 
	state = 1
	buzz(state)
	return state

# Code for the 'HUMANS AND PLANTS' state.
def humans_and_plants():
	state = 2
	buzz(state)
	return state

# Control code, which either allows the prototype to reach the 'PLANTS ONLY' state or 
# forces it to return to the 'OFF' state, depending on the time elapsed.
def plants_only_split(press_count, plants_and_humans_time_start, cur_time, state):
	if((plants_and_humans_time_start != 0) and (cur_time - plants_and_humans_time_start) > 5): 
		plants_and_humans_time_start = 0
		press_count = 0
		state = off()
	else:
		state = 3
		buzz(state)
	# The key element in the control code. The if statement checks if more than 5 seconds 
	# has elapsed since the prototype has entered the 'HUMANS AND PLANTS' state, and reacts 
	# accordingly, forcing the board to return to the 'OFF' state instead of the 'PLANTS ONLY' 
	# state it would normally otherwise reach.

	return press_count, state

# Code to control the LED brightness based on the raw input from the ADC and 
# potentiometer knob.
def change_led_brightness(raw, adc_reading_delay_start, knob, state):
	if(adc_reading_delay_start == 0):
		adc_reading_delay_start = time.monotonic()
	elif(time.monotonic() - adc_reading_delay_start > 0.01):
		raw = knob.value
		adc_reading_delay_start = 0
	# This if / elif condition forces the Pico to wait an interval of 10 milliseconds 
	# between subsequent ADC measurements. When testing, we found the LEDs would react 
	# sluggishly to changes in the potentiometer knob, as the Pico was attempting to 
	# read and use the ADC value faster than the ADC's own sampling rate. This meant 
	# that it would read and use previous ADC values instead of more recent ones. An 
	# if / elif condition was used instead of a forced time.sleep() to enhance precision - 
	# if the button was pressed during the sleep time, the Pico would be unable to respond
	# because it would still be forced to sleep. 

	if(state == 1): # 'OFF' state
		pwm_red.duty_cycle = 0
		pwm_green.duty_cycle = 0
		pwm_blue.duty_cycle = 0

	elif(state == 2): # 'HUMANS AND PLANTS' state
		if(raw < 1000): # Lower-bound cutoff, if the potentiometer knob was turned all the way
			pwm_red.duty_cycle = 0
			pwm_green.duty_cycle = 0
			pwm_blue.duty_cycle = 0
		else:
			pwm_red.duty_cycle = raw
			pwm_green.duty_cycle = raw
			pwm_blue.duty_cycle = raw
	
	else: # 'PLANTS ONLY' state
		if(raw < 1000): # Lower-bound cutoff, if the potentiometer knob was turned all the way
			pwm_red.duty_cycle = 0
			pwm_green.duty_cycle = 0
			pwm_blue.duty_cycle = 0
		else:
			pwm_red.duty_cycle = raw
			pwm_green.duty_cycle = 0
			pwm_blue.duty_cycle = raw
	return raw, adc_reading_delay_start

# The main function - this is the code that actually runs on the Pico.
if __name__ == "__main__":

	# Variable initialization
	press_count = 0 
	# Variable to count the number of times the button has been pressed. Note that button
	# presses are not the only way to update this value, the plants_only_split control code 
	# can also update this variable.

	plants_and_humans_time_start = 0 # Variable to keep track of when the 'PLANTS AND HUMANS' state is first reached.
	cur_time = 0 # Variable to keep track of the current time, for the plants_only_split if condition
	adc_reading_delay_start = 0 # Variable to keep track of the last time an ADC measurement was read.
	raw = 60000 # Raw input from the ADC measurement, also used as the LED PWM duty cycle.
	state = 1 # Variable to keep track of the state of the prototype. Set to 'OFF' by default.

	# Main control loop
	while True:
		switch.update() # Read the button's current condition (whether or not it has been pressed)
		
		# Control code, which activates if the button has been pressed. We opted to use an if 
		# condition instead of a while loop as it would be easier for the code to respond to changes 
		# in the potentiometer knob reading and adjust brightness accordingly.
		if(switch.fell): 
			press_count += 1
			cur_time = time.monotonic() # Update the current time variable

			if((press_count % 3) == 0): # The 'OFF' state
				state = off()

			elif((press_count % 3) == 1): # The 'HUMANS AND PLANTS' state
				state = humans_and_plants()
				plants_and_humans_time_start = time.monotonic()

			else: # The time-dependent state where the 'PLANTS ONLY' state is possible  
				press_count, state = plants_only_split(press_count, plants_and_humans_time_start, cur_time, state)
		
		# Read the potentiometer and change the LED brightness accordingly
		raw, adc_reading_delay_start = change_led_brightness(raw, adc_reading_delay_start, knob, state)








