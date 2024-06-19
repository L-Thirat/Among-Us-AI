import numpy as np
import cv2
from task_utility import *
import time
import pyautogui
import keyboard

click_use()
time.sleep(0.8)

dimensions = get_dimensions()
resize_images(dimensions, "Unlock Manifolds")
dimensions[0] += round(dimensions[2] / 3.4)
dimensions[1] += round(dimensions[3] / 2.9)
dimensions[2] = round(dimensions[2] / 2.4)
dimensions[3] = round(dimensions[3] / 3.1)

pos = None
for i in range(1, 11):
    while pos is None:
        pos = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Unlock Manifolds resized\\{i}.png", confidence=0.5, region=dimensions, grayscale=True)
        print(f"pos {pos}")
        if keyboard.is_pressed('1'):
            raise SystemExit(0)
    print(f"clicking")
    pyautogui.click(pos.x, pos.y)
    pos = None
