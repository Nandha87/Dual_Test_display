import time
import spidev
from gpiozero import DigitalOutputDevice
from PIL import Image, ImageDraw, ImageFont

# ---------- CONFIG ----------
WIDTH  = 320
HEIGHT = 480

DC_PIN  = 22
RST_PIN = 13
CS      = 1       # CE1
SPI_BUS = 0
SPI_SPEED = 4_000_000
# ----------------------------


class ST7796S:
    def __init__(self):
        self.dc  = DigitalOutputDevice(DC_PIN)
        self.rst = DigitalOutputDevice(RST_PIN)

        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, CS)
        self.spi.max_speed_hz = SPI_SPEED
        self.spi.mode = 0

        self.reset()
        self.init_display()

    def reset(self):
        self.rst.off()
        time.sleep(0.1)
        self.rst.on()
        time.sleep(0.2)

    def cmd(self, c):
        self.dc.off()
        self.spi.writebytes([c])

    def data(self, d):
        self.dc.on()
        self.spi.writebytes(d)

    def init_display(self):
        self.cmd(0x01)
        time.sleep(0.15)

        self.cmd(0x11)
        time.sleep(0.15)

        self.cmd(0x3A)
        self.data([0x55])  # RGB565

        self.cmd(0x36)
        self.data([0x48])

        self.cmd(0x29)
        time.sleep(0.1)

    def set_window(self):
        self.cmd(0x2A)
        self.data([0x00, 0x00, 0x01, 0x3F])  # 0–319

        self.cmd(0x2B)
        self.data([0x00, 0x00, 0x01, 0xDF])  # 0–479

        self.cmd(0x2C)

    def display(self, image):
        if image.size != (WIDTH, HEIGHT):
            image = image.resize((WIDTH, HEIGHT))

        self.set_window()

        pixels = image.convert("RGB").load()
        self.dc.on()

        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                r, g, b = pixels[x, y]
                row.append(((r & 0xF8) | (g >> 5)))
                row.append((((g & 0x1C) << 3) | (b >> 3)))
            self.spi.writebytes(row)


# ---------- DEMO ----------
disp = ST7796S()

def launch_animation(text):
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
        )
    except:
        font = ImageFont.load_default()

    for fade in range(0, 256, 16):
        img = Image.new("RGB", (WIDTH, HEIGHT), "black")
        draw = ImageDraw.Draw(img)

        draw.text(
            (WIDTH//2 - 120, HEIGHT//2 - 30),
            text,
            fill=(fade, fade, fade),
            font=font
        )

        disp.display(img)
        time.sleep(0.05)

    time.sleep(1)

launch_animation("ROZAETA")
