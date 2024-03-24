import pyautogui
import time
import pyperclip
import keyboard
def start():
    state = 0
    while True:
        if state==0:
            x,y=pyautogui.position()
            pixel=pyautogui.pixel(x,y)
            print(f"\r"+" "*100,end='')
            print(f"\r(x,y)=({x},{y}),pixel={pixel},(按alt複製位置)",end='')
            if keyboard.is_pressed("alt"):
                pyperclip.copy(f"{x},{y}")
                print(f"\r(x,y)=({x},{y}),pixel={pixel}==>位置已複製至剪貼簿(按alt繼續)",end='')
                state=1
                time.sleep(2)
        else:
            if keyboard.is_pressed("alt"):
                state = 0
                time.sleep(1)
        time.sleep(0.01)

    
    
