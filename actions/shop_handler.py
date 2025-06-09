# actions/shop_handler.py
import time
import pyautogui
from utils.logger import log_error

def process_shop():
    """
    상점 화면 처리 함수:
      - 상점 입장 후, 다음 순서로 동작을 수행합니다.
        1. "char_heal.png" 버튼 클릭
        2. 0.5초 대기
        3. "char_heal_all.png" 버튼 클릭
        4. 0.5초 대기
        5. "choice_return.png" 버튼 클릭
        6. 0.5초 대기
        7. "shop_exit.png" 버튼 클릭하여 상점 화면 종료
      - 추후 아이템 구매 작업 등이 추가될 수 있으므로 관련 처리 시 주의합니다.
    """
    log_error("[Shop Handler] 상점 화면 처리 시작")
    try:
        # 1. "char_heal.png" 버튼 클릭
        pos = pyautogui.locateCenterOnScreen("images/char_heal.png", confidence=0.6)
        if pos:
            pyautogui.click(pos)
            log_error(f"[Shop Handler] char_heal.png 클릭됨 at {pos}")
        else:
            log_error("[Shop Handler] char_heal.png 미검출")
        time.sleep(0.5)

        # 2. "char_heal_all.png" 버튼 클릭
        pos = pyautogui.locateCenterOnScreen("images/char_heal_all.png", confidence=0.6)
        if pos:
            pyautogui.click(pos)
            log_error(f"[Shop Handler] char_heal_all.png 클릭됨 at {pos}")
        else:
            log_error("[Shop Handler] char_heal_all.png 미검출")
        time.sleep(0.5)

        # 3. "choice_return.png" 버튼 클릭 → 선택지 관련 화면 종료 처리
        pos = pyautogui.locateCenterOnScreen("images/choice_return.png", confidence=0.6)
        if pos:
            pyautogui.click(pos)
            log_error(f"[Shop Handler] choice_return.png 클릭됨 at {pos}")
        else:
            log_error("[Shop Handler] choice_return.png 미검출")
        time.sleep(0.5)

        # 4. "shop_exit.png" 버튼 클릭 → 상점 맵 종료
        pos = pyautogui.locateCenterOnScreen("images/shop_exit.png", confidence=0.6)
        if pos:
            pyautogui.click(pos)
            log_error(f"[Shop Handler] shop_exit.png 클릭됨 at {pos}")
        else:
            log_error("[Shop Handler] shop_exit.png 미검출")
        time.sleep(0.5)

        # 추가: shop_exit 클릭 후 0.5초 대기, reset_confirm.png가 보이면 클릭
        pos = pyautogui.locateCenterOnScreen("images/reset_confirm.png", confidence=0.6)
        if pos:
            pyautogui.click(pos)
            log_error(f"[Shop Handler] reset_confirm.png 클릭됨 at {pos}")
        else:
            log_error("[Shop Handler] reset_confirm.png 미검출")
        time.sleep(0.5)
        
    except Exception as e:
        log_error("[Shop Handler] 예외 발생: " + str(e))
