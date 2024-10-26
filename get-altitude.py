import smbus2
import time

# Define I2C address for the barometer (0x77)
BARO_ADDRESS = 0x77

# Define barometer registers
PRESS_OUT_XL = 0x28 | 0x80  # The 0x80 is to enable auto-increment
PRESS_OUT_L = 0x29
PRESS_OUT_H = 0x2A
CTRL_REG1 = 0x20

# Initialize I2C (SMBus 1)
bus = smbus2.SMBus(1)

# Enable the barometer by setting CTRL_REG1 (0x90 enables at 12.5Hz)
bus.write_byte_data(BARO_ADDRESS, CTRL_REG1, 0x90)

# Function to read raw pressure data from the sensor
def read_pressure():
    # Read the three pressure output registers
    data = bus.read_i2c_block_data(BARO_ADDRESS, PRESS_OUT_XL, 3)
    raw_pressure = (data[2] << 16) | (data[1] << 8) | data[0]

    # Handle possible signed 24-bit value
    if raw_pressure & 0x800000:  # if the sign bit is set (negative number)
        raw_pressure -= 1 << 24

    # Convert raw pressure to hPa
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
    time.sleep(3)  # Delay 3 second between readings