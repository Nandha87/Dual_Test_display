from gpiozero import DigitalOutputDevice, DigitalInputDevice
import spidev
import smbus
import time

# LCD control pins
LCD_DC  = DigitalOutputDevice(22)
LCD_RST = DigitalOutputDevice(17)
LCD_BL  = DigitalOutputDevice(4)

# Touch pins
TP_INT = DigitalInputDevice(4)
TP_RST = DigitalOutputDevice(6)

# SPI (CE1 = GPIO7 handled by spidev)
spi = spidev.SpiDev()
spi.open(0, 1)  # SPI0, CE1
spi.max_speed_hz = 32000000

# I2C touch
i2c = smbus.SMBus(1)
TP_ADDR = 0x38  # FT6336U

def lcd_reset():
    LCD_RST.on()
    time.sleep(0.1)
    LCD_RST.off()
    time.sleep(0.1)
    LCD_RST.on()
    time.sleep(0.1)
    print("LCD reset OK")

def backlight(on=True):
    LCD_BL.on() if on else LCD_BL.off()

def read_touch():
    try:
        data = i2c.read_i2c_block_data(TP_ADDR, 0x02, 5)
        print("Touch raw:", data)
    except Exception as e:
        print("Touch error:", e)

try:
    lcd_reset()
    backlight(True)

    while True:
        read_touch()
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
