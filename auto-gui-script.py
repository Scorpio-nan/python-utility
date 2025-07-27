import pyautogui
import time

# 开始按钮
kaishi_btn = [1441, 837]
# 技能按钮
jineng_btn = [1296, 487]
# 确认按钮 
queren_btn = [1480, 806]

while True:
    print(pyautogui.position(), '鼠标位置')
    time.sleep(1)
    pyautogui.click(kaishi_btn[0], kaishi_btn[1])  # 点击开始按钮
    time.sleep(1)
    pyautogui.click(jineng_btn[0], jineng_btn[1])  # 点击技能按钮
    time.sleep(1)
    pyautogui.click(queren_btn[0], queren_btn[1])  # 点击技能按钮
    pyautogui.click(queren_btn[0], queren_btn[1])  # 点击技能按钮
