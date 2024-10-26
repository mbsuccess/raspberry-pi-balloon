import smbus2
import time

# Define I2C address for the barometer (0x77)
BARO_ADDRESS = 0x77

# Define barometer registers
PRESS_OUT_XL = 0x28
PRESS_OUT_L = 0x29
PRESS_OUT_H = 0x2A
CTRL_REG1 = 0x20

# Initialize I2C (SMBus 1)
bus = smbus2.SMBus(1)

# Enable the barometer by setting CTRL_REG1
# 0x90 enables the barometer at 12.5Hz output rate
bus.write_byte_data(BARO_ADDRESS, CTRL_REG1, 0x90)

# Function to read raw pressure data from the sensor
def read_pressure():
    # Read the three pressure output registers
    xl = bus.read_byte_data(BARO_ADDRESS, PRESS_OUT_XL)
    l = bus.read_byte_data(BARO_ADDRESS, PRESS_OUT_L)
    h = bus.read_byte_data(BARO_ADDRESS, PRESS_OUT_H)

    # Combine the registers into a single 24-bit value
    raw_pressure = (h << 16) | (l << 8) | xl

    # Convert raw pressure to Pa (assuming standard calibration)
    pressure = raw_pressure / 4096.0  # Convert to hPa
    return pressure

# Function to calculate altitude from pressure (simple approximation)
def calculate_altitude(pressure, sea_level_pressure=1013.25):
    # Use the barometric formula to estimate altitude
    altitude = 44330.0 * (1.0 - (pressure / sea_level_pressure) ** (1/5.255))
    return altitude

# Main loop to retrieve and display altitude
while True:
    pressure = read_pressure()
    altitude = calculate_altitude(pressure)
    print(f"Pressure: {pressure:.2f} hPa, Altitude: {altitude:.2f} meters")
    time.sleep(1)  # Delay 1 second between readings

