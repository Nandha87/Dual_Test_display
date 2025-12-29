from ui import UIEngine
from screens import home_screen, show_notification
from smbus2 import SMBus
import spidev
import RPi.GPIO as GPIO
import time

# --------------------
# LCD (SPI) Setup
# --------------------
DC = 25
RST = 17
CS = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(DC, GPIO.OUT)
GPIO.setup(RST, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 32000000


def lcd_cmd(cmd):
    GPIO.output(DC, 0)
    spi.writebytes([cmd])


def lcd_data(data):
    GPIO.output(DC, 1)
    spi.writebytes([data])


def lcd_init():
    GPIO.output(RST, 1)
    time.sleep(0.1)
    GPIO.output(RST, 0)
    time.sleep(0.1)
    GPIO.output(RST, 1)

    lcd_cmd(0x11)  # Sleep Out
    time.sleep(0.12)
    lcd_cmd(0x29)  # Display On


def lcd_show(img):
    pixel_bytes = img.tobytes()
    lcd_cmd(0x2C)
    GPIO.output(DC, 1)
    spi.writebytes(list(pixel_bytes))


# --------------------
# TOUCH SETUP (FT6336U)
# --------------------
bus = SMBus(1)
ADDR = 0x38  # Touch chip I2C address


def get_touch():
    try:
        data = bus.read_i2c_block_data(ADDR, 0x02, 5)
    except:
        return None

    touches = data[0] & 0x0F
    if touches == 0:
        return None

    x = ((data[1] & 0x0F) << 8) | data[2]
    y = ((data[3] & 0x0F) << 8) | data[4]
    return (x, y)


# --------------------
# UI SYSTEM
# --------------------
ui = UIEngine()
ui.set_screen(home_screen)


def handle_ui_touch(x, y):
    # Messages
    if 20 < x < 140 and 80 < y < 160:
        show_notification(ui, "Opening Messages")

    # Camera
    elif 180 < x < 300 and 80 < y < 160:
        show_notification(ui, "Opening Camera")

    # Clock
    elif 20 < x < 140 and 200 < y < 280:
        show_notification(ui, "Opening Clock")

    # Settings
    elif 180 < x < 300 and 200 < y < 280:
        show_notification(ui, "Opening Settings")

    lcd_show(ui.redraw())


ui.on_touch(handle_ui_touch)


# --------------------
# MAIN LOOP
# --------------------
lcd_init()
lcd_show(ui.redraw())

print("Rozaeta UI Running...")


while True:
    pos = get_touch()
    if pos:
        x, y = pos
        ui.handle_touch(x, y)
    time.sleep(0.05)
