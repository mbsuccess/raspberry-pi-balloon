import requests
import time
import RPi.GPIO as GPIO

# Setup GPIO pins for flashing LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # GPIO 4 for flashing
GPIO.setup(23, GPIO.OUT)  # GPIO 23 for flashing

# Ensure both LEDs are off at the start
GPIO.output(4, GPIO.LOW)
GPIO.output(23, GPIO.LOW)

# Function to flash a GPIO pin on for 1 second and then off
def flash_led(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn on LED
    time.sleep(1)                # Wait for 1 second
    GPIO.output(pin, GPIO.LOW)    # Turn off LED

# Function to get GPS data from the GPS service
def get_gps_data():
    try:
        response = requests.get('http://localhost:5000/gps')
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve GPS data")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to GPS service: {e}")
        return None

# Main function to get GPS data and flash LEDs
def main():
    try:
        while True:
            # Get GPS data
            gps_data = get_gps_data()

            if gps_data:
                latitude = gps_data.get("latitude")
                longitude = gps_data.get("longitude")
                altitude = gps_data.get("altitude")
                
                # Display GPS data
                print(f"Current Latitude: {latitude}")
                print(f"Current Longitude: {longitude}")
                print(f"Current Altitude: {altitude:.2f} feet")

            # Flash GPIO4 for 1 second
            flash_led(4)

            # Flash GPIO23 for 1 second
            flash_led(23)

            # Repeat the cycle

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Clean up GPIO settings before exiting
        GPIO.cleanup()

if __name__ == "__main__":
    main()