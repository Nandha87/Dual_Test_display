#!/usr/bin/env python3
"""
3.5" LCD + Touch Controller Test - Raspberry Pi 5 Compatible
Wiring:
- LCD_DC  → GPIO22  
- LCD_RST → GPIO17
- LCD_BL  → 5V Pin4 (always on)
- LCD_CS  → GPIO7/CE1 (SPI)
- TP_INT  → GPIO4
- TP_RST  → GPIO6  
- TP_SDA  → GPIO2 (I2C)
- TP_SCL  → GPIO3 (I2C)
"""

from gpiozero import DigitalOutputDevice, DigitalInputDevice
import spidev
import smbus
import time

# GPIO Setup (gpiozero handles Pi 5 automatically)
LCD_DC = DigitalOutputDevice(22)
LCD_RST = DigitalOutputDevice(17)
TP_INT = DigitalInputDevice(4, pull_up=True)
TP_RST = DigitalOutputDevice(6)

# SPI Setup (LCD)
spi = spidev.SpiDev()
spi.open(0, 1)  # Bus 0, CE1 (GPIO7)
spi.max_speed_hz = 32000000
spi.mode = 0

# I2C Setup (Touch - address from your i2cdetect)
i2c_bus = smbus.SMBus(1)
TP_ADDR = 0x15  # Your FT6336U touch controller

def lcd_reset():
    """Reset LCD sequence"""
    LCD_RST.on()
    time.sleep(0.01)
    LCD_RST.off()
    time.sleep(0.01)
    LCD_RST.on()
    time.sleep(0.01)
    print("✅ LCD Reset Complete")

def touch_read():
    """Read touch controller data"""
    try:
        data = i2c_bus.read_i2c_block_data(TP_ADDR, 0x00, 7)
        print(f"📱 Touch: {data}")
        return data
    except Exception as e:
        print(f"❌ Touch read error: {e}")
        return None

def main():
    print("🚀 Starting 3.5" LCD + Touch Test...")
    
    # Initialize
    lcd_reset()
    
    print("📡 Touch monitoring active (Ctrl+C to exit)...")
    print("-" * 50)
    
    try:
        while True:
            touch_data = touch_read()
            if touch_data and touch_data[0] != 176:  # 0xB0 = no touch
                print("👆 TOUCH DETECTED!")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("
👋 Exiting...")
    finally:
        spi.close()
        LCD_RST.close()
        LCD_DC.close()
        TP_RST.close()

if __name__ == "__main__":
    main()
