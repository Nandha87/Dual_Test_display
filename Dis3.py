import spidev
import time
import os

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 1)          # CE1
spi.max_speed_hz = 16000000
spi.mode = 0

# GPIO numbers
DC = 22
RST = 17

# GPIO helpers
def gpio_export(pin):
    if not os.path.exists(f"/sys/class/gpio/gpio{pin}"):
        os.system(f"echo {pin} > /sys/class/gpio/export")
        time.sleep(0.05)
    os.system(f"echo out > /sys/class/gpio/gpio{pin}/direction")

def gpio_write(pin, val):
    os.system(f"echo {val} > /sys/class/gpio/gpio{pin}/value")

def dc_cmd():  gpio_write(DC, 0)
def dc_data(): gpio_write(DC, 1)
def rst_low(): gpio_write(RST, 0)
def rst_high(): gpio_write(RST, 1)

# Export GPIOs
gpio_export(DC)
gpio_export(RST)

print("LCD Test Start")

# Reset LCD
rst_low()
time.sleep(0.1)
rst_high()
time.sleep(0.1)

# Init sequence (ST7796 / ILI9488 style)
dc_cmd()
spi.xfer2([0x11])   # Sleep out
time.sleep(0.12)

dc_cmd()
spi.xfer2([0x36])
dc_data()
spi.xfer2([0x00])

dc_cmd()
spi.xfer2([0x3A])
dc_data()
spi.xfer2([0x55])   # RGB565

dc_cmd()
spi.xfer2([0x29])   # Display ON

print("Screen ON")

# Fill red screen
dc_cmd()
spi.xfer2([0x2C])   # Memory write
dc_data()

for _ in range(5000):
    spi.xfer2([0xF8, 0x00])  # RED in RGB565

print("Red background")
time.sleep(2)
