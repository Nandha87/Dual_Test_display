import curses
from evdev import InputDevice, ecodes

TOUCH_DEV = "/dev/input/event8"

menu = [
    "Start Test",
    "Settings",
    "About",
    "Exit"
]

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    selected = 0

    dev = InputDevice(TOUCH_DEV)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "Touch Menu (Text Only)", curses.A_BOLD)

        for i, item in enumerate(menu):
            y = 2 + i
            if i == selected:
                stdscr.addstr(y, 4, item, curses.A_REVERSE)
            else:
                stdscr.addstr(y, 4, item)

        stdscr.refresh()

        for event in dev.read():
            if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_MT_POSITION_Y:
                y = int(event.value * len(menu) / 4096)
                if 0 <= y < len(menu):
                    selected = y

            if event.type == ecodes.EV_KEY and event.value == 1:
                if menu[selected] == "Exit":
                    return
                stdscr.addstr(h-2, 2, f"Selected: {menu[selected]}")
                stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
