import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0, 0)          # CE0
spi.max_speed_hz = 16000000
spi.mode = 0

DC = 22
RST = 17

def gpio(pin, val):
    os.system(f"echo {val} > /sys/class/gpio/gpio{pin}/value")

def export(pin):
    if not os.path.exists(f"/sys/class/gpio/gpio{pin}"):
        os.system(f"echo {pin} > /sys/class/gpio/export")
        time.sleep(0.05)
    os.system(f"echo out > /sys/class/gpio/gpio{pin}/direction")

export(DC)
export(RST)

def cmd(c):
    gpio(DC, 0)
    spi.xfer2([c])

def data(d):
    gpio(DC, 1)
    spi.xfer2(d if isinstance(d, list) else [d])

# Reset
gpio(RST, 0)
time.sleep(0.1)
gpio(RST, 1)
time.sleep(0.1)

# Init (ST7796 safe)
cmd(0x11)
time.sleep(0.12)

cmd(0x36)
data(0x00)

cmd(0x3A)
data(0x55)  # RGB565

cmd(0x29)

# Set address window 320x480
cmd(0x2A)
data([0x00,0x00, 0x01,0x3F])

cmd(0x2B)
data([0x00,0x00, 0x01,0xDF])

cmd(0x2C)

# Fill RED
gpio(DC, 1)
for _ in range(320 * 480):
    spi.xfer2([0xF8, 0x00])

print("RED SCREEN DONE")
