import cv2
import numpy as np
import pyautogui

# 스크린샷 저장 및 불러오기
screenshot = pyautogui.screenshot()
screenshot.save("temp_screenshot.png")
screen_img = cv2.imread("temp_screenshot.png", cv2.IMREAD_GRAYSCALE)

# 템플릿 이미지 불러오기 (map_choice 예)
template = cv2.imread("images/map_choice.png", cv2.IMREAD_GRAYSCALE)
result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
_, max_val, _, _ = cv2.minMaxLoc(result)
print("map_choice 매칭 점수:", max_val)
