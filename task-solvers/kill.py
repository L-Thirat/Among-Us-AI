from task_utility import *
import copy
import pyautogui
import time

# DEPRECIATED

def get_kill_button_pos() -> tuple:
    dimensions = get_dimensions()
    # print(round(dimensions[2] / 1.08))
    # print(round(dimensions[3] / 1.49))
    x = dimensions[0] + 1007
    y = dimensions[1] + 891
    return (x,y)

def can_kill() -> bool:
    x,y = get_kill_button_pos()
    col = pyautogui.pixel(x, y)
    return col[0] > 150 and col[1] > 150 and col[2] > 150

def kill() -> None:
    if not can_kill():
        return
    wake()
    pyautogui.click(get_kill_button_pos())