import RPi.GPIO as GPIO
import time

# GPIO pin setup
BUTTON_PIN = 23  # GPIO pin where the button is connected
LED_PIN = 4      # GPIO pin where the LED or device is connected

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set to input with pull-up resistor
GPIO.setup(LED_PIN, GPIO.OUT)  # LED pin set to output

# Function to detect button press
def detect_button():
    try:
        while True:
            button_state = GPIO.input(BUTTON_PIN)
            
            if button_state == GPIO.LOW:  # Button is pressed (closed circuit)
                print("Button pressed! Powering on GPIO 4.")
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED (GPIO 4)
            else:
                GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED (GPIO 4)

            # Small delay to debounce the button
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        GPIO.cleanup()  # Clean up GPIO on exit

if __name__ == "__main__":
    detect_button()