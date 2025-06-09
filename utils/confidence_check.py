import cv2
import numpy as np
import pyautogui
from utils.logger import log_error


def get_template_confidence(template_path, region=None):
    """
    지정된 이미지 파일(template_path)에 대해, 화면(region이 지정되었다면 해당 영역)
    의 스크린샷과 비교해서 매칭 정확도(최대 상관 계수)를 반환합니다.
    """
    # 화면 캡쳐 (region이 없으면 전체화면)
    screenshot = pyautogui.screenshot(region=region)
    screen_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        log_error(f"템플릿 이미지 로드 실패: {template_path}")
        return 0.0
    
    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val