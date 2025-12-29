import spidev
import RPi.GPIO as GPIO
import time
from smbus2 import SMBus
from PIL import Image, ImageDraw, ImageFont

# ---------------- GPIO ----------------
DC = 22
RST = 17
BL = 5

TP_INT = 4
TP_RST = 6
I2C_ADDR = 0x38

GPIO.setmode(GPIO.BCM)
GPIO.setup([DC, RST, BL, TP_RST], GPIO.OUT)
GPIO.setup(TP_INT, GPIO.IN)

GPIO.output(BL, 1)

# ---------------- SPI ----------------
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 40000000
spi.mode = 0

# ---------------- I2C ----------------
bus = SMBus(1)

# ---------------- LCD Helpers ----------------
def cmd(c):
    GPIO.output(DC, 0)
    spi.writebytes([c])

def data(d):
    GPIO.output(DC, 1)
    spi.writebytes(d if isinstance(d, list) else [d])

def lcd_reset():
    GPIO.output(RST, 0)
    time.sleep(0.1)
    GPIO.output(RST, 1)
    time.sleep(0.1)

def lcd_init():
    lcd_reset()
    cmd(0x11)
    time.sleep(0.12)
    cmd(0x36); data(0x48)
    cmd(0x3A); data(0x55)
    cmd(0x29)

def lcd_set_window(x0, y0, x1, y1):
    cmd(0x2A)
    data([x0>>8, x0&0xFF, x1>>8, x1&0xFF])
    cmd(0x2B)
    data([y0>>8, y0&0xFF, y1>>8, y1&0xFF])
    cmd(0x2C)

def lcd_draw_image(img):
    img = img.convert("RGB")
    pixels = img.load()
    lcd_set_window(0, 0, 319, 479)

    GPIO.output(DC, 1)
    buf = []
    for y in range(480):
        for x in range(320):
            r, g, b = pixels[x, y]
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            buf.append(rgb565 >> 8)
            buf.append(rgb565 & 0xFF)
        spi.writebytes(buf)
        buf.clear()

# ---------------- Touch ----------------
def touch_reset():
    GPIO.output(TP_RST, 0)
    time.sleep(0.05)
    GPIO.output(TP_RST, 1)
    time.sleep(0.2)

def get_touch():
    try:
        d = bus.read_i2c_block_data(I2C_ADDR, 0x02, 5)
        if d[0] & 0x0F:
            x = ((d[1] & 0x0F) << 8) | d[2]
            y = ((d[3] & 0x0F) << 8) | d[4]
            return x, y
    except:
        pass
    return None

# ---------------- UI ----------------
WIDTH, HEIGHT = 320, 480
font = ImageFont.load_default()
typed_text = ""

keys = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
    ["SPACE", "CLEAR"]
]

def draw_ui():
    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    d = ImageDraw.Draw(img)

    d.text((10, 10), typed_text, fill="white", font=font)

    y = 80
    for row in keys:
        x = 10
        for key in row:
            w = 60 if key in ["SPACE", "CLEAR"] else 30
            d.rectangle([x, y, x+w, y+40], outline="white")
            d.text((x+5, y+12), key, fill="white", font=font)
            x += w + 5
        y += 50

    return img

def key_pressed(x, y):
    y0 = 80
    for row in keys:
        x0 = 10
        for key in row:
            w = 60 if key in ["SPACE", "CLEAR"] else 30
            if x0 < x < x0+w and y0 < y < y0+40:
                return key
            x0 += w + 5
        y0 += 50
    return None

# ---------------- Main ----------------
lcd_init()
touch_reset()

while True:
    img = draw_ui()
    lcd_draw_image(img)

    t = get_touch()
    if t:
        tx, ty = t
        key = key_pressed(tx, ty)
        if key:
            if key == "SPACE":
                typed_text += " "
            elif key == "CLEAR":
                typed_text = ""
            else:
                typed_text += key
            time.sleep(0.3)
