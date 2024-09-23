import requests
import time
from datetime import datetime
import RPi.GPIO as GPIO

# Function to calculate time difference in seconds
def calculate_time_difference(previous_time_str, current_time_str):
    fmt = '%Y-%m-%d %H:%M:%S'
    previous_time = datetime.strptime(previous_time_str, fmt)
    current_time = datetime.strptime(current_time_str, fmt)
    return (current_time - previous_time).total_seconds()

# Setup GPIO pins for rising and falling indicators
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # GPIO 4 for rising
GPIO.setup(23, GPIO.OUT)  # GPIO 23 for falling

# Ensure both LEDs are off at the start
GPIO.output(4, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

# Function to handle LED status based on altitude changes
def handle_led_status(rising, falling):
    if rising:
        GPIO.output(4, GPIO.HIGH)  # Light up GPIO4 (Rising)
        print("gpio4 ON, now setting gpio23 off")
        GPIO.output(23, GPIO.LOW)  # Turn off GPIO23
    elif falling:
        GPIO.output(4, GPIO.LOW)   # Turn off GPIO4
        print("gpio4 OFF, now setting gpio23 ON")
        GPIO.output(23, GPIO.HIGH) # Light up GPIO23 (Falling)
    else:
        GPIO.output(4, GPIO.LOW)   # Turn off both LEDs
        GPIO.output(23, GPIO.LOW)
        print("both GPIOs off")

# Main function to check GPS service
def check_gps_service():
    previous_altitude = None
    previous_timestamp = None
    
    try:
        while True:
            try:
                # Query the GPS service
                response = requests.get('http://localhost:5000/gps')
                if response.status_code == 200:
                    gps_data = response.json()
                    current_altitude = gps_data["altitude"]
                    current_timestamp = gps_data["lastFetch"]
                    
                    # Print the current altitude
                    print(f"Current Altitude: {current_altitude:.2f} feet")

                    if previous_altitude is not None and previous_timestamp is not None:
                        # Compare current and previous altitudes
                        altitude_difference = current_altitude - previous_altitude
                        
                        # Calculate time difference between the current and previous GPS fetch times
                        time_difference = calculate_time_difference(previous_timestamp, current_timestamp)
                        
                        if time_difference > 0:  # Avoid division by zero
                            # Calculate feet per second
                            feet_per_second = altitude_difference / time_difference
                            
                            # Determine if rising or falling
                            if feet_per_second > 0:
                                print(f"Rising at {feet_per_second:.2f} feet/second")
                                handle_led_status(rising=True, falling=False)
                            elif feet_per_second < 0:
                                print(f"Falling at {-feet_per_second:.2f} feet/second")
                                handle_led_status(rising=False, falling=True)
                            else:
                                print("No altitude change")
                                handle_led_status(rising=False, falling=False)
                    else:
                        handle_led_status(rising=False, falling=False)  # No data yet
                    
                    # Update previous values for the next iteration
                    previous_altitude = current_altitude
                    previous_timestamp = current_timestamp

                else:
                    print("Failed to retrieve GPS data")
                    handle_led_status(rising=False, falling=False)  # Turn off LEDs on error

                # Wait for 5 seconds before the next check
                time.sleep(5)

            except requests.exceptions.RequestException as e:
                print(f"Error connecting to GPS service: {e}")
                handle_led_status(rising=False, falling=False)  # Turn off LEDs on error
                break

    except KeyboardInterrupt:
        print("Exiting...")
        
    finally:
        # Clean up GPIO settings before exiting
        GPIO.cleanup()

if __name__ == "__main__":
    check_gps_service()