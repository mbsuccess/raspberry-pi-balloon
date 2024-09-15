import RPi.GPIO as GPIO # type: ignore
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
led_pin = 12            # GPIO12 (BCM)

GPIO.setup(led_pin, GPIO.OUT)

# Blink the LED 10 times
for _ in range(10):
    GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
    time.sleep(1)                    # Wait for 1 second
    GPIO.output(led_pin, GPIO.LOW)   # Turn LED off
    time.sleep(0.5)                  # Wait for 0.5 second

# Cleanup
GPIO.cleanup()  # Reset all GPIO pins