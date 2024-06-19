from task_utility import *
import time
import copy
import pyautogui

dimensions = get_dimensions()
resize_images(dimensions, "Fix Wiring")
left_dimensions = copy.deepcopy(dimensions)

left_dimensions[0] += round(left_dimensions[2] / 3.8) - 91
left_dimensions[2] /= 18
left_dimensions[2] = round(left_dimensions[2])
left_dimensions[1] += round(dimensions[2] / 9.6)
left_dimensions[3] /= 1.5
left_dimensions[3] = round(left_dimensions[3])

print("left_dimensions")
print(left_dimensions)

right_dimensions = copy.deepcopy(left_dimensions)
right_dimensions[0] += round(dimensions[2] / 2.4) +210

print("right_dimensions")
print(right_dimensions)

click_use()
time.sleep(0.8)

screenshot = get_screenshot(dimensions)

wire_colors = ["red", "blue", "yellow", "pink"]

for color in wire_colors:
    confidence = 0.7
    if color == "yellow":
        confidence = 0.4
    left = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Fix Wiring resized\\{color}Wire.png", confidence=confidence, region=left_dimensions)
    print("left")
    print(left)
    if not left:
        break

    pyautogui.moveTo(left[0] + round(dimensions[2] / 32), left[1])
    right = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Fix Wiring resized\\{color}Wire.png", confidence=confidence, region=right_dimensions)
    print("right")
    print(right)

    pyautogui.dragTo(right[0] - round(dimensions[2] / 19.2), right[1], duration=0.2, tween=pyautogui.easeOutQuad)
