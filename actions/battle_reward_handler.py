import time
import pyautogui
from utils.logger import log_error, log_info

def safe_locate_center(image_path, confidence=0.75):
    """
    pyautogui.locateCenterOnScreen을 호출할 때 이미지가 없으면 발생하는
    ImageNotFoundException 예외를 잡아서 None을 반환하는 안전한 함수.
    """
    try:
        return pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        # 이미지 못 찾음 (정상 상황)
        return None
    except Exception as e:
        log_error(f"[Battle] 이미지 탐색 중 오류 발생: {image_path} - {e}")
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



def card_reward():
    import global_state
    preset = f"images/reward_preset_{global_state.CURRENT_PRESET.lower()}.png"
    
    preset_gift = safe_locate_center(preset)

    if preset_gift:
        pyautogui.click(preset_gift)
        log_info(f"[card_reward] {preset} 클릭됨 at {preset_gift}")
    else:
        log_error(f"[card_reward] {preset} 미검출")

        # 2. fallback 이미지들 순차 탐색
        fallback_images = ["images/reward_gift.png", "images/reward_cost.png", "images/reward_ego.png"]
        selected = None
        for image in fallback_images:
            pos = safe_locate_center(image)
            if pos:
                pyautogui.click(pos)
                log_info(f"[card_reward] fallback 이미지 {image} 클릭됨 at {pos}")
                selected = True
                break
        
        if not selected:
            log_error("[card_reward] fallback 이미지들 모두 미검출")

            except_popup_confirm = safe_locate_center("images/popup_confirm.png")
            if except_popup_confirm:
                pyautogui.click(except_popup_confirm)
                log_info(f"[card_reward] popup_confirm.png 클릭됨 at {except_popup_confirm}")
            else:
                log_error("[card_reward] popup_confirm.png 미검출")
            return  # 다음 단계로 진행하지 않음

    time.sleep(3)
    # 3. 최종 보상 클릭 (공통)
    reward_confirm = safe_locate_center("images/battle_reward.png")
    if reward_confirm:
        pyautogui.click(reward_confirm)
        log_info(f"[card_reward] battle_reward.png 클릭됨 at {reward_confirm}")
    else:
        log_error("[card_reward] battle_reward.png 미검출")

    time.sleep(1.5)

    popup_reward_confirm = safe_locate_center("images/battle_reward.png")
    if popup_reward_confirm:
        pyautogui.click(popup_reward_confirm)
        log_info(f"[card_reward] battle_reward.png 클릭됨 at {popup_reward_confirm}")
    else:
        log_error("[card_reward] battle_reward.png 미검출")
        


    time.sleep(3)
    return True

def select_ego_gift():
    import global_state
    preset = f"images/preset_{global_state.CURRENT_PRESET.lower()}_gift.png"
    
    # 1. reward_preset 이미지 클릭 시도
    preset_pos = safe_locate_center(preset)
    if preset_pos:
        pyautogui.click(preset_pos)
        log_info(f"[select_ego_gift] {preset} 클릭됨 at {preset_pos}")

        time.sleep(2.5)  # 2.5초 대기

        confirm_pos = safe_locate_center("images/stage_clear_reward_confirm.png")
        if confirm_pos:
            pyautogui.click(confirm_pos)
            log_info(f"[select_ego_gift] stage_clear_reward_confirm.png 클릭됨 at {confirm_pos}")
        else:
            log_error("[select_ego_gift] stage_clear_reward_confirm.png 미검출")

        return True
    else:
        log_error(f"[select_ego_gift] {preset} 미검출")

    # 2. get_new_gift 이미지 클릭 → stage_clear_reward_confirm 클릭
    new_gift_pos = safe_locate_center("images/get_new_gift.png")
    if new_gift_pos:
        pyautogui.click(new_gift_pos)
        log_info(f"[select_ego_gift] get_new_gift.png 클릭됨 at {new_gift_pos}")
        time.sleep(1)

        stage_confirm_pos = safe_locate_center("images/stage_clear_reward_confirm.png")
        if stage_confirm_pos:
            pyautogui.click(stage_confirm_pos)
            log_info(f"[select_ego_gift] stage_clear_reward_confirm.png 클릭됨 at {stage_confirm_pos}")
        else:
            log_error("[select_ego_gift] stage_clear_reward_confirm.png 미검출")

        # reward_confirm 클릭 시도
        time.sleep(2)
        reward_confirm_pos = safe_locate_center("images/reward_confirm.png")
        if reward_confirm_pos:
            pyautogui.click(reward_confirm_pos)
            log_info(f"[select_ego_gift] reward_confirm.png 클릭됨 at {reward_confirm_pos}")
        else:
            log_error("[select_ego_gift] reward_confirm.png 미검출")
        
        return True

    # 3. battle_reward_popup 클릭 → reset_confirm 클릭
    popup_pos = safe_locate_center("images/battle_reward_popup.png")
    if popup_pos:
        pyautogui.click(popup_pos)
        log_info(f"[select_ego_gift] battle_reward_popup.png 클릭됨 at {popup_pos}")
        time.sleep(1)

        reset_confirm_pos = safe_locate_center("images/reset_confirm.png")
        if reset_confirm_pos:
            pyautogui.click(reset_confirm_pos)
            log_info(f"[select_ego_gift] reset_confirm.png 클릭됨 at {reset_confirm_pos}")
        else:
            log_error("[select_ego_gift] reset_confirm.png 미검출")
    else:
        log_error("[select_ego_gift] battle_reward_popup.png 미검출")

    return True
        
def get_ego_gift():
    time.sleep(0.5)
    popup_gift_pos = safe_locate_center("images/popup_confirm.png")
    if popup_gift_pos:
        pyautogui.click(popup_gift_pos)
        log_info(f"[get_ego_gift] popup_confirm.png 클릭됨 at {popup_gift_pos}")
        time.sleep(1)
    else:
        log_error("[get_ego_gift] popup_confirm.png 미검출")

    return True