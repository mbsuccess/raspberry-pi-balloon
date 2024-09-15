import os
import glob
import time

# Base directory for the 1-Wire device
base_dir = '/sys/bus/w1/devices/'
# Path to the temperature sensor data
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

# Main loop to continuously read temperature and convert to Fahrenheit
while True:
    temp_c = read_temp()
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    print(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
    time.sleep(1)

    