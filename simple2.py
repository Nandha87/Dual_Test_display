import pygame
from evdev import InputDevice, ecodes
import threading

# CHANGE THIS to your FT6336U event
TOUCH_EVENT = "/dev/input/event2"

# Screen size (change if needed)
WIDTH, HEIGHT = 320, 480

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("LCD Touch Demo")

font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

bg_color = (0, 0, 0)
touch_pos = (WIDTH // 2, HEIGHT // 2)

def touch_thread():
    global touch_pos, bg_color
    dev = InputDevice(TOUCH_EVENT)

    x = y = 0
    for event in dev.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_MT_POSITION_X:
                x = event.value
            elif event.code == ecodes.ABS_MT_POSITION_Y:
                y = event.value
                touch_pos = (x, y)
                bg_color = (0, 120, 255)  # blue on touch

touch = threading.Thread(target=touch_thread, daemon=True)
touch.start()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            running = False

    screen.fill(bg_color)
    text = font.render("Touch Screen Demo", True, (255, 255, 255))
    screen.blit(text, (40, 40))
    pygame.draw.circle(screen, (255, 0, 0), touch_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
