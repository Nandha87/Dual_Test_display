import spidev
import time
from gpiozero import DigitalOutputDevice

DC  = DigitalOutputDevice(25)
RST = DigitalOutputDevice(27)
BL  = DigitalOutputDevice(18)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 16_000_000
spi.mode = 0

def cmd(c):
    DC.off()
    spi.xfer2([c])

def data(d):
    DC.on()
    spi.xfer2(d)

# Reset
RST.off()
time.sleep(0.1)
RST.on()
time.sleep(0.1)
BL.on()

# Init (generic for SSD1331/ST7735 style)
cmd(0x11)  # sleep out
time.sleep(0.12)
cmd(0x29)  # display on

# Fill screen with red
cmd(0x2C)
DC.on()
for _ in range(128 * 64):
    spi.xfer2([0xF8, 0x00])  # RED (RGB565)

print("0.96 LCD test done")
