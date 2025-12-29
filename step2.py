import spidev, time, lgpio

DC=22; RST=17; BL=5
h=lgpio.gpiochip_open(0)
for p in (DC,RST,BL):
    lgpio.gpio_claim_output(h,p)

lgpio.gpio_write(h,BL,1)

spi=spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=16000000
spi.mode=0

def cmd(c):
    lgpio.gpio_write(h,DC,0)
    spi.writebytes([c])

def data(*d):
    lgpio.gpio_write(h,DC,1)
    spi.writebytes(list(d))

lgpio.gpio_write(h,RST,0); time.sleep(0.1)
lgpio.gpio_write(h,RST,1); time.sleep(0.12)

cmd(0x11); time.sleep(0.12)      # Sleep out
cmd(0x3A); data(0x66)            # 🔥 18-bit mode (ILI9488)
cmd(0x36); data(0x48)
cmd(0x29)

cmd(0x2A); data(0,0,1,0x3F)
cmd(0x2B); data(0,0,1,0xDF)
cmd(0x2C)

lgpio.gpio_write(h,DC,1)
for _ in range(320*480):
    spi.writebytes([255,0,0])    # RED (RGB888)

print("ILI9488 test")
