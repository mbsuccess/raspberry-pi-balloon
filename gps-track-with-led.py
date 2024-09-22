import gps
import time
import RPi.GPIO as GPIO

# Function to convert meters to feet
def meters_to_feet(meters):
    return meters * 3.28084

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # GPIO 4 for rising altitude
GPIO.setup(17, GPIO.OUT)  # GPIO 17 for falling altitude

# Function to blink LED
def blink_led(pin, cycles):
    for _ in range(cycles):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)

# Initialize GPS session
session = gps.gps(mode=gps.WATCH_ENABLE)

# Store the previous altitude in feet
previous_altitude_feet = None

try:
    while True:
        # Get the next GPS report
        report = session.next()

        # Check if the GPS report contains altitude data
        if hasattr(report, 'altMSL'):
            current_altitude_meters = report.altMSL
            current_altitude_feet = meters_to_feet(current_altitude_meters)

            # Print the current coordinates and altitude
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                print(f"Latitude: {report.lat}, Longitude: {report.lon}, Altitude: {current_altitude_feet:.2f} feet")

            # Compare with the previous altitude
            if previous_altitude_feet is not None:
                altitude_difference = current_altitude_feet - previous_altitude_feet
                if altitude_difference > 0:
                    print(f"Rose {altitude_difference:.2f} feet")
                    blink_led(4, 3)  # Blink LED on GPIO 4 for 3 cycles
                elif altitude_difference < 0:
                    print(f"Fell {-altitude_difference:.2f} feet")
                    blink_led(17, 3)  # Blink LED on GPIO 17 for 3 cycles
                else:
                    print("Altitude unchanged")
            
            # Update previous altitude
            previous_altitude_feet = current_altitude_feet

        # Wait for 3 seconds before the next reading
        time.sleep(3)

except KeyboardInterrupt:
    print("Stopping GPS script.")

finally:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()