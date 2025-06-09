# actions/choice_handler.py
import time
import pyautogui
from utils.logger import log_error, log_info


def safe_click(pos):
    if pos is None:
        return
    try:
        x, y = int(pos[0]), int(pos[1])
        pyautogui.click(x, y)
    except Exception as e:
        log_error(f"[safe_click] 클릭 에러: {e}")


def safe_locate_center(image_path, confidence=0.7):
    try:
        pos = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if pos:
            return (int(pos[0]), int(pos[1]))
    except pyautogui.ImageNotFoundException:
        log_error(f"[safe_locate_center] 이미지 미검출: {image_path}")
    except Exception as e:
        log_error(f"[safe_locate_center] 예외 발생: {e} (이미지: {image_path})")
    return None


def wait_for_image(image_path, confidence=0.6, timeout=2.0, polling_interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        pos = safe_locate_center(image_path, confidence)
        if pos:
            return pos
        time.sleep(polling_interval)
    log_error(f"[wait_for_image] 타임아웃 - 이미지 미검출: {image_path}")
    return None


def initial_choice_setup():
    log_error("[Choice Handler 초기 설정] 초기 선택지 진입 동작 시작")
    time.sleep(1)

    skip_pos = wait_for_image("images/choice_skip.png", confidence=0.6, timeout=2.0)
    if skip_pos:
        safe_click(skip_pos)
        log_error(f"[Choice Handler 초기 설정] 첫 번째 choice_skip 클릭됨 at {skip_pos}")
    else:
        log_error("[Choice Handler 초기 설정] 첫 번째 choice_skip 미검출")

    time.sleep(0.5)

    screen_w, screen_h = pyautogui.size()
    center = (screen_w // 2, screen_h // 2)

    for i in range(3):
        safe_click(center)
        log_error(f"[Choice Handler 초기 설정] 화면 중앙 클릭 {i+1}/3 at {center}")
        time.sleep(0.3)

    skip_pos = wait_for_image("images/choice_skip.png", confidence=0.6, timeout=2.0)
    if skip_pos:
        safe_click(skip_pos)
        log_error(f"[Choice Handler 초기 설정] 두 번째 choice_skip 클릭됨 at {skip_pos}")
    else:
        log_error("[Choice Handler 초기 설정] 두 번째 choice_skip 미검출")

    time.sleep(0.5)
    safe_click(center)
    log_error(f"[Choice Handler 초기 설정] 화면 중앙 단 1회 클릭 at {center}")
    time.sleep(0.5)


def post_action(skip_return=False):
    screen_w, screen_h = pyautogui.size()
    center = (screen_w // 2, screen_h // 2)

    if skip_return:
        try:
            safe_click((200, 200))
            time.sleep(0.3)
            safe_click((200, 200))
            log_error(f"[Choice Handler 후속(예외)] (200, 200) 좌표 두 번 클릭 완료")
        except Exception as e:
            log_error(f"[Choice Handler 후속(예외)] (200, 200) 클릭 에러: {e}")
    else:
        # 기존 후속 동작 유지
        skip_pos = wait_for_image("images/choice_skip.png", confidence=0.6, timeout=3.0)
        if skip_pos is not None:
            try:
                safe_click(skip_pos)
                log_error(f"[Choice Handler 후속] choice_skip.png 클릭됨 at {skip_pos}")
            except Exception as e:
                log_error(f"[Choice Handler 후속] choice_skip 클릭 에러: {e}")
        else:
            log_error("[Choice Handler 후속] choice_skip.png 미검출")
        
        time.sleep(0.5)
        for i in range(3):
            try:
                safe_click(center)
                log_error(f"[Choice Handler 후속] 화면 정중앙 클릭 {i+1}/3 at {center}")
                time.sleep(0.3)
            except Exception as e:
                log_error(f"[Choice Handler 후속] 화면 정중앙 클릭 {i+1}/3 에러: {e}")

def click_again():
    screen_w, screen_h = pyautogui.size()
    center = (screen_w // 2, screen_h // 2)
    time.sleep(0.2)
    safe_click(center)
    skip_pos = safe_locate_center("images/choice_skip.png", confidence=0.6)
    if skip_pos:
        safe_click(skip_pos)
        log_error(f"[Choice Handler] choice_skip.png 클릭됨 at {skip_pos} (루프 재시도 전)")
    else:
        log_error("[Choice Handler] choice_skip.png 미검출 (루프 재시도 전)")
    
    i = 0
    while True:
        time.sleep(0.2)
        safe_click(center)
        i += 1
        if(i >= 3):break

def process_choice():
    log_error("[Choice Handler] 선택지 처리 시작")
    initial_choice_setup()

    screen_w, screen_h = pyautogui.size()
    center = (screen_w // 2, screen_h // 2)

    while True:
        action_done = False

        # 선택지 강제 종료 조건.
        is_battle_pos = wait_for_image("images/battle_ready.png", confidence=0.8, timeout=0.7)

        if is_battle_pos and is_battle_pos != (0, 0):
            log_info(f"[choice] 전투 화면 감지 됨 at {is_battle_pos}")
            break

        is_char = wait_for_image("images/character.png", confidence=0.7, timeout=0.7)
        if is_char is not None:  
            safe_click(is_char)
            log_error(f"[Choice Handler] character.png 클릭됨 at {is_char}")
            time.sleep(2)
            action_done = True
            post_action(skip_return=False)
            continue

        is_char_1 = wait_for_image("images/character_1.png", confidence=0.6, timeout=0.7)
        if is_char_1 is not None:  
            safe_click(is_char_1)
            log_error(f"[Choice Handler] character.png 클릭됨 at {is_char_1}")
            time.sleep(2)
            action_done = True
            post_action(skip_return=False)
            continue

        is_char_2 = wait_for_image("images/character_2.png", confidence=0.6, timeout=0.7)
        if is_char_2 is not None:  
            safe_click(is_char_2)
            log_error(f"[Choice Handler] character.png 클릭됨 at {is_char_2}")
            time.sleep(2)
            action_done = True
            post_action(skip_return=False)
            continue

        # (1) "선택지" 텍스트 이미지 감지
        choice_text_pos = safe_locate_center("images/choice_text.png", confidence=0.6)
        if choice_text_pos:
            click_pos = (choice_text_pos[0], choice_text_pos[1] + 200)
            safe_click(click_pos)
            log_error(f"[Choice Handler] '선택지' 텍스트 기준 200픽셀 아래 클릭 at {click_pos}")
            action_done = True
            post_action(skip_return=False)
            continue

        # (2) choice_next.png
        next_pos = wait_for_image("images/choice_next.png", confidence=0.6, timeout=0.7)
        if next_pos:
            safe_click(next_pos)
            log_error(f"[Choice Handler] choice_next.png 클릭됨 at {next_pos}")
            time.sleep(2)
            action_done = True
            post_action(skip_return=False)
            continue

        # (3) 우선순위 선택지 이미지 검사
        priority_images = [
            "images/choice_veryhigh.png",
            "images/choice_high.png",
            "images/choice_normal.png",
            "images/choice_low.png",
            "images/choice_verylow.png"
        ]
        time.sleep(0.2)
        for img in priority_images:
            pos = safe_locate_center(img, confidence=0.8) # 선택지 이미지 신뢰성을 높이기 위해서 0.8로 높게 설정.
            if pos:
                safe_click(pos)
                log_error(f"[Choice Handler] 우선순위 선택지 이미지 {img} 클릭됨 at {pos}")
                action_done = True
                break

        # if action_done:
        #     time.sleep(0.5)
        #     select_pos = safe_locate_center("images/choice_select.png", confidence=0.6)
        #     if select_pos:
        #         safe_click(select_pos)
        #         log_error(f"[Choice Handler] choice_select.png 클릭됨 at {select_pos}")
        #     else:
        #         log_error("[Choice Handler] choice_select.png 미검출")
        #     time.sleep(1)
        #     post_action(skip_return=False)
        #     continue

        # (4) choice_select_confirm.png
        confirm_pos = wait_for_image("images/choice_select_confirm.png", confidence=0.6)
        if confirm_pos:
            safe_click(confirm_pos)
            log_error(f"[Choice Handler] choice_select_confirm.png 클릭됨 at {confirm_pos}")
            
            time.sleep(2)
            click_again()
            time.sleep(1)
            continue

        # (5) choice_return.png
        return_pos = wait_for_image("images/choice_return.png", confidence=0.6, timeout=0.7)
        if return_pos:
            safe_click(return_pos)
            log_error(f"[Choice Handler] choice_return.png 클릭됨 at {return_pos}. 선택지 종료 시도.")
            post_action(skip_return=True)
            time.sleep(5)
            break

        # 이미지 미검출 등 아무 처리도 안 된 경우:
        # "choice_skip.png" 클릭 + 0.3초 후 화면 중앙 클릭 후 루프 계속
        skip_pos = safe_locate_center("images/choice_skip.png", confidence=0.6)
        if skip_pos:
            safe_click(skip_pos)
            log_error(f"[Choice Handler] choice_skip.png 클릭됨 at {skip_pos} (루프 재시도 전)")
        else:
            log_error("[Choice Handler] choice_skip.png 미검출 (루프 재시도 전)")

        time.sleep(0.3)
        safe_click(center)
        time.sleep(0.3)
        safe_click(center)
        skip_pos = wait_for_image("images/choice_skip.png", confidence=0.6, timeout=0.7)
        if skip_pos:
            safe_click(skip_pos)
            log_error(f"[Choice Handler 초기 설정] 첫 번째 choice_skip 클릭됨 at {skip_pos}")
        else:
            log_error("[Choice Handler 초기 설정] 첫 번째 choice_skip 미검출")
        time.sleep(0.2)
        safe_click(center)
        time.sleep(0.2)
        safe_click(center)
        
        log_error(f"[Choice Handler] 화면 중앙 클릭 at {center} (루프 재시도 전)")

        time.sleep(0.5)

    log_error("[Choice Handler] 선택지 처리 완료. 화면 전환 종료")
