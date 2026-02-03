# max score reached 526, avg score 347, after some time dino misses, its ok. Game restarts automatically
# the tempo is increasing with time, well working code is a tuning / combination of jump_cooldown and scale_factor variables
# birds appear closer to score 450, some birds are very high so dont clash into dino without ducking even

import pygetwindow as gw
import pyautogui
import time
from PIL import ImageGrab

# #TODO run this code only after have chrome tab with game open (probably on another screen)

chrome_windows = [w for w in gw.getWindowsWithTitle("Dinosaur Game") if w]
if not chrome_windows:
    raise Exception("Chrome window not found!")
chrome_window = chrome_windows[0]

chrome_window.activate()
time.sleep(0.2)

## ------------ CONSTANTS ------------- ##
cactus_checking_area = (1923 + 350, 950, 1923 + 900, 950 + 140)
jump_time, last_jump, curr_jump, last_int = 0, 0, 0, 0
last_jump_time = 0
jump_cooldown = 0.04  # 0.04 sec

## --------- GAME --------------- ##
canvas_x, canvas_y = 2113, 1037  # clicking on my dino
pyautogui.click(canvas_x, canvas_y)
pyautogui.press("space")

game_on = True
while game_on:
    screenshot = ImageGrab.grab(bbox=cactus_checking_area, all_screens=True)
    pixels = screenshot.load()
    cactus = False

    x_detection_start = 2  # pixels away from dino
    full_detection_width = cactus_checking_area[2] - cactus_checking_area[0]
    # First iteration
    x_detection_end = full_detection_width

    lines_to_check = [
        screenshot.height - 5,
        screenshot.height - 20,
        screenshot.height - 40,
    ]

    if last_jump_time != 0:
        int_time = time.time() - last_jump_time  # time since last jump
        scale_factor = 400
        x_detection_end = min(
            cactus_checking_area[2] - cactus_checking_area[0],
            x_detection_start
            + scale_factor / max(int_time, 0.01),  # avoid division by zero
        )

    found = False
    for x in range(x_detection_start, int(x_detection_end)):
        for y in lines_to_check:
            r, g, b = pixels[x, y]
            if r < 120 and g < 120 and b < 120:
                cactus = True
                found = True
                break
        if found:
            break

    if cactus and time.time() - last_jump_time > jump_cooldown:
        pyautogui.press("space")
        jump_time = time.time()
        curr_jump = jump_time

        # Interval since last jump
        int_time = curr_jump - last_jump

        # Scale lookahead width dynamically: faster = bigger
        # For example, max width =  full checking area
        # min width = initial detection distance

        last_jump = jump_time
        last_int = int_time

    time.sleep(0.005)
