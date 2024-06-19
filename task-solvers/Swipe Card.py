import numpy as np
import cv2
from task_utility import *
import time
import cv2
import copy
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 2.5)
y = dimensions[1] + round(dimensions[3] / 1.32)

pyautogui.click(x,y)
time.sleep(0.8)

x = dimensions[0] + round(dimensions[2] / 3.33) - 10
y = dimensions[1] + round(dimensions[3] / 2.51)

pyautogui.moveTo(x,y)

x2 = dimensions[0] + round(dimensions[2] / 1.3) + 80
# y is the same

def easeInOutExpo(x):
    if x == 0 or x == 1:
        return x
    else:
        if x < 0.5:
            return pow(2, 20 * x - 10) / 2
        else:
            return 2 - pow(2, -20 * x + 10) / 2


duration = 1.4
pyautogui.dragTo(x2,y, duration=duration)

while not is_task_done("Swipe Card"):
    time.sleep(0.5)
    duration -= 0.1
    pyautogui.moveTo(x,y)
    pyautogui.dragTo(x2,y, duration=duration)