import spidev, time
import lgpio

DC=22; RST=17; BL=5
h = lgpio.gpiochip_open(0)
for p in (DC,RST,BL):
    lgpio.gpio_claim_output(h,p)

lgpio.gpio_write(h, BL, 1)

spi = spidev.SpiDev()
spi.open(0,1)          # CE1
spi.max_speed_hz = 1000000
spi.mode = 0

# HARD reset
lgpio.gpio_write(h, RST, 0)
time.sleep(0.2)
lgpio.gpio_write(h, RST, 1)
time.sleep(0.2)

# Spam commands
for _ in range(50):
    lgpio.gpio_write(h, DC, 0)
    spi.writebytes([0x00])
    time.sleep(0.02)

print("SPI sent")
