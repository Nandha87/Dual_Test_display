import time
import spidev
from gpiozero import DigitalOutputDevice

DC  = DigitalOutputDevice(25)
RST = DigitalOutputDevice(27)

spi = spidev.SpiDev()
spi.open(0, 0)                 # SPI0, CE0 (IMPORTANT)
spi.max_speed_hz = 2_000_000   # VERY SAFE
spi.mode = 0

def cmd(c):
    DC.off()
    spi.writebytes([c])

def data(d):
    DC.on()
    spi.writebytes(d)

# Reset
RST.off()
time.sleep(0.2)
RST.on()
time.sleep(0.2)

# Init
cmd(0x01)       # SW reset
time.sleep(0.2)

cmd(0x11)       # Sleep out
time.sleep(0.2)

cmd(0x3A)       # Pixel format
data([0x55])    # RGB565

cmd(0x36)       # Memory access
data([0x48])

cmd(0x29)       # Display ON
time.sleep(0.1)

# Full screen
cmd(0x2A)
data([0x00, 0x00, 0x01, 0x3F])   # 0–319
cmd(0x2B)
data([0x00, 0x00, 0x01, 0xDF])   # 0–479
cmd(0x2C)

# Fill RED
DC.on()
for _ in range(320 * 480):
    spi.writebytes([0xF8, 0x00])

print("If wiring is correct, screen should be RED")
