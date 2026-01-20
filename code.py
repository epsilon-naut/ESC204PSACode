from machine import Pin, PWM
from utime import sleep

def mode_1():
    pinO1.value(1)
    pinO2.value(1)
    pinO3.value(0)

def mode_2():
    pinO1.value(1)
    pinO2.value(1)
    pinO3.value(1)

def mode_3():
    pinO1.value(0)
    pinO2.value(0)
    pinO3.value(0)

led1 = 1
led2 = 2
led3 = 4
in1 = 17
#in2 = 23
in3 = 24

pinO1 = Pin(led1, Pin.OUT)
pinO2 = Pin(led2, Pin.OUT)
pinO3 = Pin(led3, Pin.OUT)

pinI = Pin(in1, Pin.IN, Pin.PULL_DOWN)
#pin5 = Pin(in2, Pin.IN, Pin.PULL_DOWN)
#pin6 = Pin(in3, Pin.IN, Pin.PULL_DOWN)

def mode_change(Pin):
    pass

#gonna need to check PWM 
if __name__ == "__main__":
    print("LED starts flashing...")
    pinI.irq(trigger = Pin.IRQ_RISING, handler = mode_change)
    while True:
        try:
            mode_1()
            sleep(1) # sleep 1sec
            mode_2()
            sleep(1)
            mode_3()
            sleep(1)
        except KeyboardInterrupt:
            break
    pinO1.off()
    print("Finished.")
