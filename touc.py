import smbus
import time

bus = smbus.SMBus(1)
TOUCH_ADDR = 0x43  # detected address

while True:
    try:
        data = bus.read_i2c_block_data(TOUCH_ADDR, 0x00, 7)
        x = ((data[1] & 0x0F) << 8) | data[2]
        y = ((data[3] & 0x0F) << 8) | data[4]
        print("Touch:", x, y)
    except Exception:
        pass
    time.sleep(0.1)
