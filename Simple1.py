import smbus
import time

bus = smbus.SMBus(1)
ADDR = 0x38

def read_touch():
    touches = bus.read_byte_data(ADDR, 0x02)
    if touches == 0:
        return None

    data = bus.read_i2c_block_data(ADDR, 0x03, 4)
    x = ((data[0] & 0x0F) << 8) | data[1]
    y = ((data[2] & 0x0F) << 8) | data[3]
    return touches, x, y

print("FT6336U touch test")

while True:
    t = read_touch()
    if t:
        print("Touches:", t[0], "X:", t[1], "Y:", t[2])
    time.sleep(0.05)
