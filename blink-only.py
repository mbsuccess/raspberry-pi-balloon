import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # GPIO 4 for the LED

# Blink LED function
def blink_led(cycles):
    for _ in range(cycles):
        GPIO.output(4, GPIO.HIGH)  # LED ON
        time.sleep(0.5)  # Wait for 0.5 seconds
        GPIO.output(4, GPIO.LOW)   # LED OFF
        time.sleep(0.3)  # Wait for 0.3 seconds

try:
    blink_led(3)  # Blink 3 cycles

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
    