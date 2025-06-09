# utils/image_tools.py
import time
import pyautogui
from utils.logger import log_error

def click_image(template_path, confidence=0.9):
    """
    이미지 탐색을 단 한 번 수행하고, 이미지를 찾으면 클릭 후 True,
    찾지 못하면 오류를 로그에 남기고 False를 반환합니다.
    """
    try:
        pos = pyautogui.locateCenterOnScreen(template_path, confidence=confidence)
        if pos:
            try:
                pyautogui.click(pos)
            except Exception as click_error:
                log_error(f"클릭 중 예외 발생 ({template_path}): {click_error}")
                # 클릭 실패해도 다음 과정으로 건너뜁니다.
            return True
        else:
            log_error(f"이미지 클릭 실패 (이미지 없음): {template_path}")
            return False
    except Exception as e:
        log_error(f"이미지 로드/탐색 중 예외 발생 ({template_path}): {e}")
        return False

def click_multiple(template_path, clicks=3, interval=0.5, confidence=0.9):
    """
    주어진 이미지에 대해 click_image가 한 번의 시도를 통해
    성공하면 interval만큼 딜레이를 두고 총 clicks번 시도합니다.
    이미지가 없으면 즉시 건너뜁니다.
    """
    for _ in range(clicks):
        try:
            if click_image(template_path, confidence):
                time.sleep(interval)
        except Exception as e:
            log_error(f"click_multiple 실행 중 예외 발생 ({template_path}): {e}")
