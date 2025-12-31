import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 16000000

def dc_cmd(): os.system('echo 0 > /sys/class/gpio/gpio22/value')
def dc_data(): os.system('echo 1 > /sys/class/gpio/gpio22/value')
def rst_high(): os.system('echo 1 > /sys/class/gpio/gpio17/value')
def rst_low(): os.system('echo 0 > /sys/class/gpio/gpio17/value')

os.system('echo 22 > /sys/class/gpio/export; echo out > /sys/class/gpio/gpio22/direction')
os.system('echo 17 > /sys/class/gpio/export; echo out > /sys/class/gpio/gpio17/direction')

print("LCD Text Test")

rst_low(); time.sleep(0.1); rst_high(); time.sleep(0.1)

dc_cmd(); spi.xfer2([0x11]); time.sleep(0.12)
dc_cmd(); spi.xfer2([0x36, 0x00])
dc_cmd(); spi.xfer2([0x3A, 0x55])
dc_cmd(); spi.xfer2([0x29])

print("Screen ON")

dc_cmd(); spi.xfer2([0x2C])
dc_data()
for i in range(5000):
    spi.xfer2([0xF8, 0x00])
print("Red background")

time.sleep(2)
print("Text ready")
