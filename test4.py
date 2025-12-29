import spidev, time, lgpio

DC=22; RST=17; BL=5
h = lgpio.gpiochip_open(0)
for p in (DC,RST,BL):
    lgpio.gpio_claim_output(h,p)

lgpio.gpio_write(h, BL, 1)

spi = spidev.SpiDev()
spi.open(0, 1)              # CE1 = GPIO7
spi.max_speed_hz = 8000000  # IMPORTANT: slow first
spi.mode = 0

def cmd(c):
    lgpio.gpio_write(h, DC, 0)
    spi.writebytes([c])

def data(*d):
    lgpio.gpio_write(h, DC, 1)
    spi.writebytes(list(d))

# HARD RESET
lgpio.gpio_write(h, RST, 0)
time.sleep(0.2)
lgpio.gpio_write(h, RST, 1)
time.sleep(0.2)

# ---- ST7796S INIT ----
cmd(0x01)      # Software reset
time.sleep(0.15)

cmd(0x11)      # Sleep out
time.sleep(0.15)

cmd(0xF0); data(0xC3)
cmd(0xF0); data(0x96)

cmd(0x36); data(0x48)   # rotation
cmd(0x3A); data(0x55)   # RGB565

cmd(0xB4); data(0x01)
cmd(0xB6); data(0x80,0x02)

cmd(0xE8); data(0x40,0x8A,0x00,0x00,0x29,0x19,0xA5,0x33)
cmd(0xC1); data(0x06)
cmd(0xC2); data(0xA7)
cmd(0xC5); data(0x18)

cmd(0xE0); data(0xF0,0x09,0x0B,0x06,0x04,0x15,0x2F,0x54,0x42,0x3C,0x17,0x14,0x18,0x1B)
cmd(0xE1); data(0xF0,0x09,0x0B,0x06,0x04,0x03,0x2D,0x43,0x42,0x3B,0x16,0x14,0x17,0x1B)

cmd(0x29)      # Display ON
time.sleep(0.1)

# ---- FILL RED ----
cmd(0x2A); data(0,0,1,0x3F)
cmd(0x2B); data(0,0,1,0xDF)
cmd(0x2C)

lgpio.gpio_write(h, DC, 1)
for _ in range(320*480):
    spi.writebytes([0xF8,0x00])

print("If you see RED → ST7796S OK")
