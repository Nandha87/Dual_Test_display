import os
import time
import pygame
from evdev import InputDevice, ecodes

# Force pygame to SPI LCD
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_VIDEODRIVER"] = "fbcon"

TOUCH_DEV = "/dev/input/event8"
WIDTH, HEIGHT = 320, 480

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 36)
screen.fill((0, 0, 0))
pygame.display.update()

dev = InputDevice(TOUCH_DEV)

print("Touch the screen")

for event in dev.read_loop():
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_MT_POSITION_X:
            x = int(event.value * WIDTH / 4096)
        elif event.code == ecodes.ABS_MT_POSITION_Y:
            y = int(event.value * HEIGHT / 4096)

            screen.fill((0, 0, 0))
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 12)
            text = font.render("Touch detected", True, (255, 255, 255))
            screen.blit(text, (60, 40))
            pygame.display.update()
