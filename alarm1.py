import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
gpio_pin = 23           # GPIO23

# Setup GPIO pin as output
GPIO.setup(gpio_pin, GPIO.OUT)

try:
    # Turn GPIO23 ON (HIGH)
    GPIO.output(gpio_pin, GPIO.HIGH)
    print("GPIO23 is ON")
    
    # Wait for 0.1 seconds
    time.sleep(3)
    
    # Turn GPIO23 OFF (LOW)
    GPIO.output(gpio_pin, GPIO.LOW)
    print("GPIO23 is OFF")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()
    print("GPIO cleanup complete")