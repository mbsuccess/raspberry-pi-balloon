import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
gpio_pin = 25           # GPIO25

# Setup GPIO pin as output
GPIO.setup(gpio_pin, GPIO.OUT)

try:
    # Turn ALARM GPIO ON (HIGH)
    GPIO.output(gpio_pin, GPIO.HIGH)
    print("GPIO" + str(gpio_pin) +" is ON")
    
    # Wait for 0.1 seconds
    time.sleep(20)
    
    # Turn GPIO23 OFF (LOW)
    GPIO.output(gpio_pin, GPIO.LOW)
    print("GPIO" + str(gpio_pin) +" is OFF")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()
    print("GPIO cleanup complete")