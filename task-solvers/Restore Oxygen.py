from task_utility import *
import time
import cv2
import pytesseract
import copy
from PIL import Image
import re

click_use()
time.sleep(0.8)

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Terus\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

dimensions = get_dimensions()

s_dimensions = copy.deepcopy(dimensions)
s_dimensions[0] = s_dimensions[0] + round(dimensions[2] / 1.59)
s_dimensions[1] = s_dimensions[1] + round(dimensions[3] / 5.74)
s_dimensions[2] = round(s_dimensions[2] / 7.16)
s_dimensions[3] = round(s_dimensions[3] / 4.39)

screenshot = get_screenshot(s_dimensions)

# rotate image so digit detection works
s2 = screenshot.rotate(335, Image.NEAREST, expand = 1).convert('L')

# get text from image
text = pytesseract.image_to_string(s2)
print(f"text: {text}")
try:
    nums = re.findall(r'\b\d+\b', text)[0]
except IndexError:
    print("This one was already done")
    nums = []

num_coords = [  [2, 1.25],
                [2.41, 2.93], [2, 2.93], [1.71, 2.93],
                [2.41, 1.99], [2, 1.99], [1.71, 1.99],
                [2.41, 1.56], [2, 1.56], [1.71, 1.56],
                [1.71, 1.25] # green
             ]

for num in nums:
    n = int(num)
    pyautogui.click(dimensions[0] + round(dimensions[2] / num_coords[n][0]), dimensions[1] + round(dimensions[3] / num_coords[n][1]))

pyautogui.click(dimensions[0] + round(dimensions[2] / num_coords[10][0]), dimensions[1] + round(dimensions[3] / num_coords[10][1]))
