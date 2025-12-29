import spidev, time
import lgpio

DC = 22
RST = 17
BL = 5

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, DC)
lgpio.gpio_claim_output(h, RST)
lgpio.gpio_claim_output(h, BL)

lgpio.gpio_write(h, BL, 1)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 24000000
spi.mode = 0

def cmd(c):
    lgpio.gpio_write(h, DC, 0)
    spi.writebytes([c])

def data(d):
    lgpio.gpio_write(h, DC, 1)
    spi.writebytes([d])

# RESET
lgpio.gpio_write(h, RST, 0)
time.sleep(0.1)
lgpio.gpio_write(h, RST, 1)
time.sleep(0.12)

# INIT
cmd(0x11)      # Sleep out
time.sleep(0.12)

cmd(0x36); data(0x00)   # TRY THIS (rotation fix)
cmd(0x3A); data(0x55)   # RGB565
cmd(0x29)      # Display ON

# FILL RED
cmd(0x2A); data(0); data(0); data(1); data(0x3F)
cmd(0x2B); data(0); data(0); data(1); data(0xDF)
cmd(0x2C)

lgpio.gpio_write(h, DC, 1)
for _ in range(320*480):
    spi.writebytes([0xF8, 0x00])

print("If RED screen → LCD OK")
