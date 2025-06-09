# result_handler.py

import time
import pyautogui
from utils.logger import log_error, log_info

def safe_locate_center(image_path, confidence=0.6):
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

def process_result_screen():
    """
    결과 화면 처리: 
      1. result_screen.png가 감지되면, 결과 화면임을 인지
      2. result_screen_confirm.png를 찾아 클릭
      3. 3초 대기 후 result_screen_reward.png 클릭
      4. 3초 대기 후 dungeon_reward.png 클릭
      5. 8초 대기 후 dungeon_reward_confirm.png 클릭
      6. 8초 대기 후 처리 종료(원래 루프로 복귀)
    """
    # 1. 결과 화면 감지 (여유있게 5초 대기, confidence는 0.7 기준)
    result_screen_pos = wait_for_image("images/result_screen.png", timeout=5, confidence=0.7)
    if result_screen_pos:
        log_info("[Result Handler] 결과 화면 감지됨: result_screen.png at " + str(result_screen_pos))
    else:
        log_error("[Result Handler] 결과 화면 미검출: result_screen.png")
        return  # 결과 화면이 감지되지 않으면 처리를 중단

    # 2. 결과 화면 확인 버튼 클릭 (result_screen_confirm.png)
    result_confirm_pos = safe_locate_center("images/result_screen_confirm.png", confidence=0.7)
    if result_confirm_pos:
        pyautogui.click(result_confirm_pos)
        log_info("[Result Handler] result_screen_confirm.png 클릭됨 at " + str(result_confirm_pos))
    else:
        log_error("[Result Handler] result_screen_confirm.png 미검출")
    time.sleep(3)

    # 3. 결과 보상 버튼 클릭 (result_screen_reward.png)
    result_reward_pos = safe_locate_center("images/result_screen_reward.png", confidence=0.7)
    if result_reward_pos:
        pyautogui.click(result_reward_pos)
        log_info("[Result Handler] result_screen_reward.png 클릭됨 at " + str(result_reward_pos))
    else:
        log_error("[Result Handler] result_screen_reward.png 미검출")
    time.sleep(3)

    # 4. 던전 보상 버튼 클릭 (dungeon_reward.png)
    dungeon_reward_pos = safe_locate_center("images/dungeon_reward.png", confidence=0.7)
    if dungeon_reward_pos:
        pyautogui.click(dungeon_reward_pos)
        log_info("[Result Handler] dungeon_reward.png 클릭됨 at " + str(dungeon_reward_pos))
    else:
        log_error("[Result Handler] dungeon_reward.png 미검출")
    time.sleep(5)

    # 5. 던전 보상 확인 버튼 클릭 (dungeon_reward_confirm.png)
    dungeon_reward_confirm_pos = safe_locate_center("images/reset_confirm.png", confidence=0.7)
    if dungeon_reward_confirm_pos:
        pyautogui.click(dungeon_reward_confirm_pos)
        log_info("[Result Handler] reset_confirm.png 클릭됨 at " + str(dungeon_reward_confirm_pos))
    else:
        log_error("[Result Handler] reset_confirm.png 미검출")
    time.sleep(8)

    pass_lv_confirm_pos = safe_locate_center("images/battle_reward.png", confidence=0.7)
    if pass_lv_confirm_pos:
        pyautogui.click(pass_lv_confirm_pos)
        log_info("[Result Handler] battle_reward.png 클릭됨 at " + str(pass_lv_confirm_pos))
    else:
        log_error("[Result Handler] battle_reward.png 미검출")
    time.sleep(8)

    

    # 처리 완료 후 (원하는 후속 동작이나 화면 감지 루프로 복귀하도록 구성)
