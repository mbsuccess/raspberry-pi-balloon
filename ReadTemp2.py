import os
import glob
import time
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
led_pin_up = 17  # LED for temperature increasing (GPIO17)
led_pin_down = 18  # LED for temperature decreasing (GPIO18)
GPIO.setup(led_pin_up, GPIO.OUT)
GPIO.setup(led_pin_down, GPIO.OUT)

# Turn both LEDs off initially
GPIO.output(led_pin_up, GPIO.LOW)
GPIO.output(led_pin_down, GPIO.LOW)

# Base directory for the 1-Wire device
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

# Function to read the raw temperature data
def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()

# Function to parse and get the temperature in Celsius
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Variable to store the last temperature
last_temp = None

# Main loop to continuously read temperature, detect changes, and control LEDs
while True:
    current_temp = read_temp()

    if last_temp is not None:
        if current_temp > last_temp:
            # Temperature is going up
            GPIO.output(led_pin_up, GPIO.HIGH)   # Turn on LED for increasing temp
            GPIO.output(led_pin_down, GPIO.LOW)  # Turn off LED for decreasing temp
            print(f"Temperature is rising: {current_temp:.2f}°C")
        elif current_temp < last_temp:
            # Temperature is going down
            GPIO.output(led_pin_up, GPIO.LOW)    # Turn off LED for increasing temp
            GPIO.output(led_pin_down, GPIO.HIGH) # Turn on LED for decreasing temp
            print(f"Temperature is falling: {current_temp:.2f}°C")
        else:
            # Temperature is constant (Optional: you can decide to turn both LEDs off)
            GPIO.output(led_pin_up, GPIO.LOW)
            GPIO.output(led_pin_down, GPIO.LOW)
            print(f"Temperature is constant: {current_temp:.2f}°C")

    # Update the last temperature value
    last_temp = current_temp

    # Wait before reading the temperature again
    time.sleep(1)

# Cleanup GPIO on exit (use try-except to handle cleanup if needed)
GPIO.cleanup()
    