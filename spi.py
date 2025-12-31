import spidev

spi = spidev.SpiDev()
spi.open(0, 0)   # try CE0 first
spi.max_speed_hz = 1000000
spi.xfer2([0xAA])
print("SPI OK")
