from gpiozero import DigitalOutputDevice, Button
import spidev
import smbus
import time

# GPIO (your wiring)
LCD_DC  = DigitalOutputDevice(22)
LCD_RST = DigitalOutputDevice(17)
TP_INT  = Button(4, pull_up=True)
TP_RST  = DigitalOutputDevice(6)

# SPI LCD
spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 20000000

# I2C Touch (0x15 from your scan)
bus = smbus.SMBus(1)
TP_ADDR = 0x15

# Simple LCD init for ST7796/ILI9486 (320x480)
def lcd_init():
    LCD_RST.off(); time.sleep(0.02)
    LCD_RST.on(); time.sleep(0.12)
    
    cmd = [0x11]  # Sleep out
    spi.xfer2([0x01, 0x11])
    time.sleep(0.12)
    
    cmd = [0x36, 0x00]  # Memory access
    spi.xfer2([0x01, 0x36, 0x00])
    
    cmd = [0x3A, 0x55]  # Pixel format 16bit
    spi.xfer2([0x01, 0x3A, 0x55])
    
    cmd = [0x29]  # Display on
    spi.xfer2([0x01, 0x29])
    print("✅ LCD Initialized")

# Fill screen red
def fill_screen(color):
    LCD_DC.on()
    spi.xfer2([0x2C] + [color] * 480)  # Start window + color

# Show touch coordinates
def show_touch(x, y):
    print(f"👆 Touch at X:{x} Y:{y}")

lcd_init()
fill_screen(0xF800)  # Red screen
print("🟢 Touch screen to see coordinates!")

try:
    while True:
        if TP_INT.is_pressed:
            try:
                # Read touch coords from FT6336 reg 0x02-0x13
                data = bus.read_i2c_block_data(TP_ADDR, 0x02, 16)
                if data[0] > 0:  # Touch detected
                    x = ((data[3] & 0x0F) << 8) | data[4]
                    y = ((data[5] & 0x0F) << 8) | data[6]
                    show_touch(x, y)
            except:
                pass
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    spi.close()
EOF
