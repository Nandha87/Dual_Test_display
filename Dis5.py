from gpiozero import DigitalOutputDevice, DigitalInputDevice
import spidev
import smbus
import time

# -----------------------------
# GPIO Setup using gpiozero
# -----------------------------
LCD_DC = DigitalOutputDevice(22)
LCD_RST = DigitalOutputDevice(17)
LCD_BL = DigitalOutputDevice(4)
# CS handled by spidev, do not manually toggle
TP_INT = DigitalInputDevice(4)
TP_RST = DigitalOutputDevice(6)

# -----------------------------
# SPI Setup (for LCD)
# -----------------------------
spi = spidev.SpiDev()
spi.open(0, 1)  # Bus 0, Device 1 (CE1)
spi.max_speed_hz = 32000000

# -----------------------------
# I2C Setup (for Touch)
# -----------------------------
i2c_bus = smbus.SMBus(1)  # I2C bus
TP_ADDR = 0x38  # Default I2C address for FT6336U

# -----------------------------
# Functions
# -----------------------------
def lcd_reset():
    LCD_RST.on()
    time.sleep(0.1)
    LCD_RST.off()
    time.sleep(0.1)
    LCD_RST.on()
    time.sleep(0.1)
    print("LCD Reset Done")

def lcd_backlight(on=True):
    if on:
        LCD_BL.on()
    else:
        LCD_BL.off()
    print("Backlight", "ON" if on else "OFF")

def touch_test():
    try:
        data = i2c_bus.read_i2c_block_data(TP_ADDR, 0, 7)
        print("Touch Data:", data)
    except Exception as e:
        print("Touch read error:", e)

# -----------------------------
# Main Test Loop
# -----------------------------
try:
    print("Starting LCD & Touch Test")
    lcd_reset()
    lcd_backlight(True)

    print("Reading Touch Input...")
    while True:
        touch_test()
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting test...")

finally:
    spi.close()
