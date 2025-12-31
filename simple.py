from gpiozero import LED
import smbus
import time

led = LED(17)
bus = smbus.SMBus(1)

print("Blink test...")
for i in range(5):
    led.on()
    time.sleep(0.2)
    led.off()
    time.sleep(0.2)
print("Blink OK")

print("Touch test...")
try:
    while True:
        data = bus.read_byte_data(0x15, 0x02)
        print("Touch:", data)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Done!")
