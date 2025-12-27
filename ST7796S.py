import time
import spidev
from gpiozero import DigitalOutputDevice

# GPIO pins
DC  = DigitalOutputDevice(22)
RST = DigitalOutputDevice(13)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 1)                 # SPI0, CE1
spi.max_speed_hz = 16_000_000
spi.mode = 0

def cmd(c):
    DC.off()
    spi.xfer2([c])

def data(d):
    DC.on()
    spi.xfer2(d)

# Reset display
RST.off()
time.sleep(0.1)
RST.on()
time.sleep(0.15)

# ---- ST7796S INIT ----
cmd(0x01)        # Software reset
time.sleep(0.15)

cmd(0x11)        # Sleep out
time.sleep(0.15)

cmd(0x3A)        # Pixel format
data([0x55])     # RGB565

cmd(0x36)        # MADCTL
data([0x48])     # orientation

cmd(0x29)        # Display ON
time.sleep(0.1)

# Set address window (320x480)
cmd(0x2A)
data([0x00, 0x00, 0x01, 0x3F])   # X: 0–319
cmd(0x2B)
data([0x00, 0x00, 0x01, 0xDF])   # Y: 0–479
cmd(0x2C)

def fill(color):
    DC.on()
    for _ in range(320 * 480):
        spi.xfer2(color)

print("ST7796S test running")

while True:
    fill([0xF8, 0x00])   # RED
    time.sleep(1)

    fill([0x07, 0xE0])   # GREEN
    time.sleep(1)

    fill([0x00, 0x1F])   # BLUE
    time.sleep(1)
