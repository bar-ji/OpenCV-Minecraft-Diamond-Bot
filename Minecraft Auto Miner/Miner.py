import pyautogui
import pydirectinput
import keyboard
import time 
from PIL import ImageGrab
import numpy as np
import cv2

time.sleep(3)
found_diamonds = False
placing_torch = False
terminated = False
torches_placed = 0

lower_range_diamond = np.array([75, 80, 100])
upper_range_diamond = np.array([90, 255, 255])
lower_range_lava = np.array([7, 216, 193])
upper_range_lava = np.array([23, 255, 255])
    
def mining_forward():
    global terminated
    if not placing_torch:
        pydirectinput.keyDown("c")
        pydirectinput.mouseDown()
        pydirectinput.keyDown("w")
    if keyboard.is_pressed("u"):
        pydirectinput.keyUp("w")
        pydirectinput.mouseUp()
        terminated = True

def timer():
    torch_time = time.time()
    screenshot_time = time.time()
    while not found_diamonds and not terminated:
        mining_forward()
        if(time.time() > torch_time + 6):
            torch_time = time.time()
            place_torch()
        if(time.time() > screenshot_time + 0.4):
            screenshot_time = time.time()
            if not placing_torch:
                detect_color()

def place_torch():
    global placing_torch
    global torches_placed
    torches_placed += 1
    if torches_placed % 64 == 0:
        pydirectinput.press(str(torches_placed / 64))     
        pydirectinput.press("f")
        pydirectinput.press("9")
    placing_torch = True
    pydirectinput.mouseUp()
    pydirectinput.moveRel(700, 400)
    pydirectinput.rightClick()
    pydirectinput.moveRel(-700, -400)
    placing_torch = False

def detect_color():
    im1 = pyautogui.screenshot("currentImg.png")
    im1 = cv2.imread("currentImg.png")
    hsv = cv2.cvtColor(cv2.UMat(im1), cv2.COLOR_BGR2HSV)
    mask_diamond = cv2.inRange(hsv, lower_range_diamond, upper_range_diamond)
    mask_lava = cv2.inRange(hsv, lower_range_lava, upper_range_lava)

    cv2.imwrite("HSV.png", hsv)
    cv2.imwrite("CurrentMaskDiamond.png", mask_diamond)
    cv2.imwrite("CurrentMaskLava.png", mask_lava)
    print("Blue pixels: " + str(cv2.countNonZero(mask_diamond)))
    print("Orange pixels: " + str(cv2.countNonZero(mask_lava)))

    if(int(cv2.countNonZero(mask_diamond)) > 5000):
        release_inputs()
        print("Found Diamonds")
        quit()
    if(int(cv2.countNonZero(mask_lava)) > 25000):
        release_inputs()
        pydirectinput.moveRel(0, -1000)
        pydirectinput.moveRel(0, -1000)
        pydirectinput.moveRel(0, -1000)
        pydirectinput.press("8")
        pydirectinput.rightClick()
        pydirectinput.press("c")
        print("Found Lava")
        quit()

def release_inputs():
    pydirectinput.keyUp("w")
    pydirectinput.mouseUp()
    
timer()
pydirectinput.keyUp("c")
