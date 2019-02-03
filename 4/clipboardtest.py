import pyperclip
import time

list = []

while True:
    if pyperclip.paste():
        value = pyperclip.paste()
        if value not in list:
            list.append(value)
        print(list)
        time.sleep(3)
