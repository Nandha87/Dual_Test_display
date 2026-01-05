import pigpio
import spidev
import smbus
import time

# GPIO numbers
LCD_DC  = 22
LCD_RST = 17
LCD_BL  = 4
TP_RST  = 6

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio not running")

# GPIO setup
for pin in [LCD_DC, LCD_RST, LCD_BL, TP_RST]:
    pi.set_mode(pin, pigpio.OUTPUT)

# SPI (CE1 = GPIO7)
spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 32000000

# I2C (FT6336U)
i2c = smbus.SMBus(1)
TP_ADDR = 0x38

def lcd_reset():
    pi.write(LCD_RST, 1)
    time.sleep(0.1)
    pi.write(LCD_RST, 0)
    time.sleep(0.1)
    pi.write(LCD_RST, 1)

def backlight(on=True):
    pi.write(LCD_BL, 1 if on else 0)

def read_touch():
    try:
        data = i2c.read_i2c_block_data(TP_ADDR, 0x02, 5)
        print("Touch:", data)
    except Exception as e:
        print("Touch error:", e)

lcd_reset()
backlight(True)

while True:
    read_touch()
    time.sleep(1)
