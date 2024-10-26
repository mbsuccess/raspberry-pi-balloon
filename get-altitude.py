import smbus2
import time

print ("starting script 3")

# I2C address for the BMP388 (0x77)
BMP388_ADDRESS = 0x77

# BMP388 Registers
BMP388_CHIP_ID_REG = 0x00  # Chip ID register
BMP388_CHIP_ID = 0x50      # Expected Chip ID for BMP388
BMP388_CTRL_MEAS = 0x1B    # Control register
BMP388_PRESS_MSB = 0x04    # Pressure MSB register
BMP388_PRESS_LSB = 0x05    # Pressure LSB register
BMP388_PRESS_XLSB = 0x06   # Pressure XLSB register

# Initialize I2C (SMBus 1)
bus = smbus2.SMBus(1)

# Read Chip ID to verify communication
chip_id = bus.read_byte_data(BMP388_ADDRESS, BMP388_CHIP_ID_REG)
if chip_id != BMP388_CHIP_ID:
    print(f"Error: Chip ID mismatch. Expected {BMP388_CHIP_ID}, but got {chip_id}.")
    exit()

# Set up the control register for normal mode
bus.write_byte_data(BMP388_ADDRESS, BMP388_CTRL_MEAS, 0x33)

# Function to read raw pressure data from BMP388
def read_pressure():
    # Read raw pressure data (20-bit unsigned)
    msb = bus.read_byte_data(BMP388_ADDRESS, BMP388_PRESS_MSB)
    lsb = bus.read_byte_data(BMP388_ADDRESS, BMP388_PRESS_LSB)
    xlsb = bus.read_byte_data(BMP388_ADDRESS, BMP388_PRESS_XLSB)
    raw_pressure = (msb << 16) | (lsb << 8) | xlsb

    # Convert raw pressure to Pa
    pressure = raw_pressure / 16.0  # Adjust for 20-bit resolution
    return pressure

# Function to calculate altitude from pressure (standard barometric formula)
def calculate_altitude(pressure, sea_level_pressure=1013.25):
    altitude = 44330.0 * (1.0 - (pressure / sea_level_pressure) ** (1/5.255))
    return altitude

# Main loop to retrieve and display pressure and altitude
while True:
    pressure = read_pressure() / 100  # Convert to hPa
    altitude = calculate_altitude(pressure)
    print(f"Pressure: {pressure:.2f} hPa, Altitude: {altitude:.2f} meters")
    time.sleep(2)