from machine import Pin
import time

# Configure onboard LED
led = Pin("P10_5", Pin.OUT)

print("LED Blink Program Started")

for count in range(10):

    led.value(1)
    print("LED ON")

    time.sleep(1)

    led.value(0)
    print("LED OFF")

    time.sleep(1)