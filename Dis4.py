import spidev
import time
import os
from PIL import Image, ImageDraw, ImageFont
import smbus

# -------------------------
# SPI Setup
spi = spidev.SpiDev()
spi.open(0, 1)          # CE1
spi.max_speed_hz = 16000000
spi.mode = 0

# GPIO Setup
DC = 22
RST = 17

def gpio_export(pin):
    if not os.path.exists(f"/sys/class/gpio/gpio{pin}"):
        os.system(f"echo {pin} > /sys/class/gpio/export")
        time.sleep(0.05)
    os.system(f"echo out > /sys/class/gpio/gpio{pin}/direction")

def gpio_write(pin, val):
    os.system(f"echo {val} > /sys/class/gpio/gpio{pin}/value")

gpio_export(DC)
gpio_export(RST)

def cmd(c):
    gpio_write(DC, 0)
    spi.xfer2([c])

def data(d):
    gpio_write(DC, 1)
    if isinstance(d, list):
        spi.xfer2(d)
    else:
        spi.xfer2([d])

# -------------------------
# LCD Reset
gpio_write(RST, 0)
time.sleep(0.1)
gpio_write(RST, 1)
time.sleep(0.1)

# -------------------------
# ST7796S Initialization
cmd(0x11)  # Sleep Out
time.sleep(0.12)

cmd(0x36)  # MADCTL
data(0x00)  # Normal rotation, RGB

cmd(0x3A)  # Interface Pixel Format
data(0x55)  # RGB565

cmd(0x29)  # Display ON

# Set full window 320x480
cmd(0x2A)
data([0x00, 0x00, 0x01, 0x3F])  # X:0-319
cmd(0x2B)
data([0x00, 0x00, 0x01, 0xDF])  # Y:0-479
cmd(0x2C)  # Memory Write

# -------------------------
# Fill screen red
gpio_write(DC, 1)
for _ in range(320*480):
    spi.xfer2([0xF8, 0x00])  # RGB565 red (high byte, low byte)

# -------------------------
# Draw text using PIL
# Create an image in RGB565 size
img = Image.new("RGB", (320, 480), color=(255, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()
draw.text((50, 220), "Hello Rozaeta!", font=font, fill=(255, 255, 255))

# Convert PIL image to RGB565 bytes
def image_to_data(img):
    data = []
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            data.append((rgb565 >> 8) & 0xFF)
            data.append(rgb565 & 0xFF)
    return data

img_data = image_to_data(img)

# Write to display
chunk = 4096
for i in range(0, len(img_data), chunk):
    gpio_write(DC, 1)
    spi.xfer2(img_data[i:i+chunk])

print("Text drawn!")

# -------------------------
# -------------------------
# FT6336U Touch Setup
bus = smbus.SMBus(1)
TOUCH_ADDR = 0x43  # detected I2C address

def read_touch():
    try:
        data = bus.read_i2c_block_data(TOUCH_ADDR, 0x00, 7)
        x = ((data[1] & 0x0F) << 8) | data[2]
        y = ((data[3] & 0x0F) << 8) | data[4]
        return (x, y)
    except:
        return None

print("Touch ready! Tap screen to see coordinates:")

while True:
    t = read_touch()
    if t:
        print("Touch:", t)
    time.sleep(0.1)
