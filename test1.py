import time
import spidev
from gpiozero import DigitalOutputDevice

# ===== MATCH YOUR WIRING =====
DC  = DigitalOutputDevice(22)   # GPIO22 → LCD_DC
RST = DigitalOutputDevice(17)   # GPIO17 → LCD_RST

spi = spidev.SpiDev()
spi.open(0, 1)                  # SPI0, CE1 (GPIO7)
spi.max_speed_hz = 2_000_000    # Safe speed
spi.mode = 0
# ============================

def cmd(c):
    DC.off()
    spi.writebytes([c])

def data(d):
    DC.on()
    spi.writebytes(d)

# ---- RESET ----
RST.off()
time.sleep(0.2)
RST.on()
time.sleep(0.2)

# ---- INIT ST7796S ----
cmd(0x01)        # Software reset
time.sleep(0.15)

cmd(0x11)        # Sleep out
time.sleep(0.15)

cmd(0x3A)        # Pixel format
data([0x55])     # RGB565

cmd(0x36)        # MADCTL
data([0x48])     # Landscape / RGB

cmd(0x29)        # Display ON
time.sleep(0.1)

# ---- FULL SCREEN ----
cmd(0x2A)
data([0x00, 0x00, 0x01, 0x3F])  # X: 0–319
cmd(0x2B)
data([0x00, 0x00, 0x01, 0xDF])  # Y: 0–479
cmd(0x2C)

# ---- FILL RED ----
DC.on()
for _ in range(320 * 480):
    spi.writebytes([0xF8, 0x00])  # RED

print("If wiring is correct, screen should be RED")
