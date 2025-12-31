import RPi.GPIO as GPIO
import spidev
import smbus
import time

# -----------------------------
# GPIO Setup
# -----------------------------
# LCD Pins
LCD_DC = 22
LCD_RST = 17
LCD_BL = 4
LCD_CS = 7  # CE1

# Touch Pins
TP_INT = 4
TP_RST = 6

# GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(LCD_DC, GPIO.OUT)
GPIO.setup(LCD_RST, GPIO.OUT)
GPIO.setup(LCD_BL, GPIO.OUT)
GPIO.setup(LCD_CS, GPIO.OUT)
GPIO.setup(TP_INT, GPIO.IN)
GPIO.setup(TP_RST, GPIO.OUT)

# -----------------------------
# SPI Setup (for LCD)
# -----------------------------
spi = spidev.SpiDev()
spi.open(0, 1)  # SPI bus 0, CE1 (GPIO7)
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
    GPIO.output(LCD_RST, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(LCD_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(LCD_RST, GPIO.HIGH)
    time.sleep(0.1)

def lcd_backlight(on=True):
    GPIO.output(LCD_BL, GPIO.HIGH if on else GPIO.LOW)

def touch_test():
    try:
        data = i2c_bus.read_i2c_block_data(TP_ADDR, 0, 7)
        print("Touch Data:", data)
    except Exception as e:
        print("Touch read error:", e)

# -----------------------------
# Main Test
# -----------------------------
try:
    print("Resetting LCD...")
    lcd_reset()
    print("Turning on Backlight...")
    lcd_backlight(True)

    # Test touch input
    print("Testing Touch Controller...")
    while True:
        touch_test()
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting test...")
finally:
    GPIO.cleanup()
    spi.close()
