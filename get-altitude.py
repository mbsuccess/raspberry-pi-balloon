#!/usr/bin/python
import time
import smbus

print ("this is crap")

class BMP388:
    def __init__(self, address=0x77):
        self._address = address
        self._bus = smbus.SMBus(1)
        self._initialize_sensor()
        self._load_calibration()

    def _initialize_sensor(self):
        if self._read_byte(0x00) == 0x50:
            self._write_byte(0x7E, 0xB6)  # Soft reset
            time.sleep(0.01)
            self._write_byte(0x1B, 0x33)  # Enable pressure and temperature in normal mode
        else:
            raise RuntimeError("Sensor initialization failed")

    def _load_calibration(self):
        self.T1 = self._read_u16(0x31)
        self.T2 = self._read_u16(0x33)
        self.T3 = self._read_s8(0x35)
        self.P1 = self._read_s16(0x36)
        self.P2 = self._read_s16(0x38)
        self.P3 = self._read_s8(0x3A)
        self.P4 = self._read_s8(0x3B)
        self.P5 = self._read_u16(0x3C)
        self.P6 = self._read_u16(0x3E)
        self.P7 = self._read_s8(0x40)
        self.P8 = self._read_s8(0x41)
        self.P9 = self._read_s16(0x42)
        self.P10 = self._read_s8(0x44)
        self.P11 = self._read_s8(0x45)

    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)

    def _read_s8(self, cmd):
        result = self._read_byte(cmd)
        return result - 256 if result > 127 else result

    def _read_u16(self, cmd):
        return (self._read_byte(cmd + 1) << 8) + self._read_byte(cmd)

    def _read_s16(self, cmd):
        result = self._read_u16(cmd)
        return result - 65536 if result > 32767 else result

    def compensate_temperature(self, adc_T):
        var1 = (adc_T / 16384.0 - self.T1 / 1024.0) * self.T2
        var2 = (adc_T / 131072.0 - self.T1 / 8192.0) * self.T3
        self.T_fine = var1 + var2
        return self.T_fine / 5120.0

    def compensate_pressure(self, adc_P):
        var1 = (self.T_fine / 2.0) - 64000.0
        var2 = var1 * var1 * self.P6 / 32768.0
        var2 = var2 + var1 * self.P5 * 2.0
        var2 = (var2 / 4.0) + (self.P4 * 65536.0)
        var1 = (self.P3 * var1 * var1 / 524288.0 + self.P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.P1
        if var1 == 0.0:
            return 0  # Avoid division by zero
        pressure = 1048576.0 - adc_P
        pressure = (pressure - var2 / 4096.0) * 6250.0 / var1
        var1 = self.P9 * pressure * pressure / 2147483648.0
        var2 = pressure * self.P8 / 32768.0
        pressure = pressure + (var1 + var2 + self.P7) / 16.0
        return pressure

    def get_sensor_data(self):
        adc_T = (self._read_byte(0x09) << 16) + (self._read_byte(0x08) << 8) + self._read_byte(0x07)
        adc_P = (self._read_byte(0x06) << 16) + (self._read_byte(0x05) << 8) + self._read_byte(0x04)
        temperature = self.compensate_temperature(adc_T)
        pressure = self.compensate_pressure(adc_P)
        altitude = 44330.0 * (1.0 - (pressure / 101325.0) ** 0.1903)
        return temperature, pressure, altitude

if __name__ == '__main__':
    sensor = BMP388()
    while True:
        temperature, pressure, altitude = sensor.get_sensor_data()
        print(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa, Altitude: {altitude:.2f} m")
        time.sleep(1)

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