import spidev
import time
from gpiozero import DigitalOutputDevice

# ---------- SMALL DISPLAY (ST7735S) ----------
SMALL_DC  = DigitalOutputDevice(25)
SMALL_RST = DigitalOutputDevice(27)

spi_small = spidev.SpiDev()
spi_small.open(0, 0)          # CE0
spi_small.max_speed_hz = 16_000_000
spi_small.mode = 0

def small_cmd(c):
    SMALL_DC.off()
    spi_small.xfer2([c])

def small_data(d):
    SMALL_DC.on()
    spi_small.xfer2(d)

def init_st7735():
    SMALL_RST.off()
    time.sleep(0.1)
    SMALL_RST.on()
    time.sleep(0.1)

    small_cmd(0x11)   # sleep out
    time.sleep(0.12)
    small_cmd(0x29)   # display on

def small_fill(color):
    small_cmd(0x2C)
    SMALL_DC.on()
    for _ in range(160 * 80):
        spi_small.xfer2(color)

# ---------- MAIN DISPLAY (ST7796S) ----------
MAIN_DC  = DigitalOutputDevice(22)
MAIN_RST = DigitalOutputDevice(13)

spi_main = spidev.SpiDev()
spi_main.open(0, 1)          # CE1
spi_main.max_speed_hz = 30_000_000
spi_main.mode = 0

def main_cmd(c):
    MAIN_DC.off()
    spi_main.xfer2([c])

def main_data(d):
    MAIN_DC.on()
    spi_main.xfer2(d)

def init_st7796():
    MAIN_RST.off()
    time.sleep(0.1)
    MAIN_RST.on()
    time.sleep(0.1)

    main_cmd(0x11)  # sleep out
    time.sleep(0.12)
    main_cmd(0x29)  # display on

def main_fill(color):
    main_cmd(0x2C)
    MAIN_DC.on()
    for _ in range(320 * 480):
        spi_main.xfer2(color)

# ---------- RUN BOTH ----------
init_st7735()
init_st7796()

print("Both displays active")

while True:
    # Small display → text / status color
    small_fill([0xFF, 0xE0])   # yellow

    # Main display → UI background
    main_fill([0x00, 0x1F])    # blue

    time.sleep(2)

    small_fill([0xF8, 0x00])   # red
    main_fill([0x07, 0xE0])    # green

    time.sleep(2)
