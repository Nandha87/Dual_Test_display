cat > simple_test.py << 'EOF'
#!/usr/bin/env python3
from gpiozero import LED, Button
import smbus
import time

# Super simple - just blink + touch
led = LED(17)      # LCD_RST as blink test
btn = Button(4)    # TP_INT as touch button
bus = smbus.SMBus(1)

print("🟢 GPIO OK - Touch screen or Ctrl+C")

def blink():
    print("💡 Blink test...")
    for i in range(5):
        led.on(); time.sleep(0.2); led.off(); time.sleep(0.2)
    print("✅ Blink OK")

blink()

print("📱 Touch test (0x15)...")
try:
    while True:
        data = bus.read_byte_data(0x15, 0x02)
        print(f"Touch reg: {data}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("✅ Done!")
EOF
