import ctypes
import win32gui
import pyautogui
import os
import pydirectinput
from wake_keyboard import wake
from PIL import Image

ctypes.windll.user32.SetProcessDPIAware()

with open("sendDataDir.txt") as f:
    line = f.readline().rstrip()
    SEND_DATA_PATH = line + "\\sendData.txt"

SABOTAGE_TASKS = ["Reset Reactor", "Fix Lights", "Fix Communications", "Restore Oxygen"]


def getGameData():
    dataLen: int = 10
    x, y, status, tasks, task_locations, task_steps, map_id, dead = None, None, None, None, None, None, None, None
    while True:
        with open(SEND_DATA_PATH) as file:
            lines = file.readlines()
            if len(lines) < dataLen:
                file.close()
                continue

            x = float(lines[0].split()[0])
            y = float(lines[0].split()[1])
            status = lines[1].strip()

            tasks = lines[2].rstrip().strip('][').split(", ")

            task_locations = lines[3].rstrip().strip('][').split(", ")

            task_steps = lines[4].rstrip().strip('][').split(", ")

            map_id = lines[5].rstrip()

            dead = bool(int(lines[6].rstrip()))

            room = lines[10].rstrip()

        if None in [x, y, status, tasks, task_locations, task_steps, map_id, dead, room]:
            continue
        break

    if dead or status == "impostor":
        if tasks[0] == "Submit Scan" and task_locations[0] == "Hallway":
            tasks.pop(0)
            task_locations.pop(0)
    return {"position": (x, y), "status": status, "tasks": tasks, "task_locations": task_locations,
            "task_steps": task_steps, "map_id": map_id, "dead": dead, "room": room}


def get_screenshot(dimensions=None, window_title="Among Us"):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd and not dimensions:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            im.save("tmp1.png")
            return im
        elif dimensions:
            im = pyautogui.screenshot(region=dimensions)
            im.save("tmp2.png")
            return im
        else:
            print('Window not found!')
    else:
        im = pyautogui.screenshot()
        im.save("tmp.png")
        return im


def get_dimensions():
    window_title = "Among Us"
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        return [x, y, x1, y1]
    else:
        print('Window not found!')


def click_use():
    wake()
    dim = get_dimensions()
    pydirectinput.moveTo(dim[0] + dim[2] - round(dim[2] / 13), dim[1] + dim[3] - round(dim[3] / 7))
    pydirectinput.click()
    return


def resize_images(dimensions, task_name):
    if task_name == "Unlock Manifolds":
        for i in range(1, 11):
            loaded_img = Image.open(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name}\\{i}.png")
            new_img = loaded_img.resize(
                (round(loaded_img.width * (dimensions[2] / 1920)), round(loaded_img.height * (dimensions[3] / 1080))))
            new_img.save(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name} resized\\{i}.png")

    elif task_name == "Fix Wiring":
        wire_colors = ["red", "blue", "yellow", "pink"]
        for color in wire_colors:
            loaded_img = Image.open(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name}\\{color}Wire.png")
            new_img = loaded_img.resize(
                (round(loaded_img.width * (dimensions[2] / 1920)), round(loaded_img.height * (dimensions[3] / 1080))))
            new_img.save(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name} resized\\{color}Wire.png")

    elif task_name == "Stabilize Steering":
        loaded_img = Image.open(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name}\\crosshair.png")
        new_img = loaded_img.resize(
            (round(loaded_img.width * (dimensions[2] / 1920)), round(loaded_img.height * (dimensions[3] / 1080))))
        new_img.save(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name} resized\\crosshair.png")

    elif task_name == "Inspect Sample":
        loaded_img = Image.open(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name}\\anomaly.png")
        new_img = loaded_img.resize(
            (round(loaded_img.width * (dimensions[2] / 1920)), round(loaded_img.height * (dimensions[3] / 1080))))
        new_img.save(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name} resized\\anomaly.png")

    elif task_name == "close":
        loaded_img = Image.open(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name}\\closeX.png")
        new_img = loaded_img.resize(
            (round(loaded_img.width * (dimensions[2] / 1920)), round(loaded_img.height * (dimensions[3] / 1080))))
        new_img.save(f"{get_dir()}\\task-solvers\\cv2-templates\\{task_name} resized\\closeX.png")


def get_dir():
    return os.getcwd()


def click_close():
    wake()
    dim = get_dimensions()
    resize_images(dim, "close")
    center = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\close resized\\closeX.png",
                                            confidence=0.7, grayscale=True)
    pydirectinput.moveTo(center[0], center[1])
    pydirectinput.click()
    return


def get_screen_coords():
    while True:
        print(pyautogui.position(), end='\r')


def get_screen_ratio(dim):
    while True:
        print(round(abs(dim[2] / (pyautogui.position().x - dim[0])), 2),
              round(abs(dim[3] / (pyautogui.position().y - dim[1])), 2), end='\r')


def is_task_done(task):
    data = getGameData()

    try:
        if task in SABOTAGE_TASKS:
            if task in data["tasks"]:
                return False
            return True

        index = data["tasks"].index(task)
        steps = data["task_steps"][index].split('/')
        return steps[0] == steps[1]

    # Index error on new ver
    except (IndexError, ValueError) as e:
        if task == "Reset Reactor" or task == "Reset Seismic Stabilizers":
            return not ("Reset Reactor" in data["tasks"] or "Reset Seismic Stabilizers" in data["tasks"])
        print("Index / Value error")
        print(task)
        print(data["tasks"])
        print(data["task_steps"])
        print(e)
        return False


def is_urgent_task() -> bool:
    data = getGameData()
    if data["dead"]:
        return False

    urgent_tasks = ["Reset Reactor", "Restore Oxygen", "Reset Seismic Stabilizers"]
    for task in urgent_tasks:
        if task in data['tasks']:
            return True
    return False