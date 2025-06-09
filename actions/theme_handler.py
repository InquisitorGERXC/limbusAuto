# actions/theme_handler.py
import time
import pyautogui
from utils.logger import log_error, log_info
from screen_detector import get_current_state
from utils.confidence_check import get_template_confidence



# actions/theme_handler.py 내 select_theme_pack() 수정 예시
def select_theme_pack():
    try:
        theme_select = pyautogui.locateCenterOnScreen("images/theme_select.png", confidence=0.3)
        if not theme_select:
            log_error("테마 선택 화면이 감지되지 않음: images/theme_select.png")
            return
    except Exception as e:
        log_error("테마 선택 화면 검출 중 예외 발생: " + str(e))
        return

    time.sleep(3)
    selected = False
    chosen_template = ""
    for i in range(1, 46):
        theme_filename = f"images/theme_{i}.png"
        try:

            pos = pyautogui.locateCenterOnScreen(theme_filename, confidence=0.72)
            confidence_val = get_template_confidence(theme_filename)
            log_info(f"테마 이미지 {theme_filename}: 위치={pos}, 정확도={confidence_val:.2f}")
        except Exception as e:
            log_error(f"테마 이미지 {theme_filename} 검출 중 예외 발생: {e}")
            continue
        
        if pos:
            try:
                pyautogui.moveTo(pos)
                pyautogui.mouseDown()
                pyautogui.dragRel(0, 450, duration=0.5)
                pyautogui.mouseUp()
                chosen_template = theme_filename
                log_error(f"테마 선택 완료: {theme_filename}")
                selected = True
                break
            except Exception as e:
                log_error(f"테마 선택 드래그 중 오류 발생 ({theme_filename}): {e}")
    if not selected:
        log_error("화면에 적절한 테마팩이 감지되지 않음.")

    # 테마 선택 후 로그와 대기
    log_error("테마 선택 완료 후 4초 대기 - 맵 화면 전환 대기")
    time.sleep(4)

    # 선택 후 현재 화면 상태 재점검
    state = get_current_state()  # get_current_state()를 호출해 현재 상태를 확인
    log_error("테마 선택 후 현재 상태: " + state)

    

