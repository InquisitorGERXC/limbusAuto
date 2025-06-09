# actions/battle_handler.py
import time
import pyautogui
import global_state
from utils.logger import log_error, log_info, log_warning

from preset_config import get_preset_characters

# 전역 상태 변수: 해당 전투 세션에서 편성이 완료되었는지 여부
formation_done = False

def safe_locate_center(image_path, confidence=0.7):
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

def run_formation():
    """
    전투 지역 입장 후 편성 화면에서 수행해야 할 초기 작업들:
      - "초기화" 버튼 클릭, "확인" 버튼 클릭
      - 프리셋에 따라 캐릭터 편성
      - "전투 시작" 버튼 클릭 등
    이 함수는 편성 과정을 전부 수행합니다.
    """
    log_error("[Battle] 편성 화면: 초기화 버튼 클릭 시도")
    reset_btn_pos = safe_locate_center("images/reset_button.png")
    if reset_btn_pos:
        pyautogui.click(reset_btn_pos)
        time.sleep(0.5)
        log_info("[Battle] 초기화 버튼 클릭 완료")
    else:
        log_error("[Battle] 초기화 버튼 미검출")

    log_error("[Battle] 편성 화면: 초기화 확인 버튼 클릭 시도")
    reset_confirm_pos = safe_locate_center("images/reset_confirm.png")
    if reset_confirm_pos:
        pyautogui.click(reset_confirm_pos)
        time.sleep(0.5)
        log_info("[Battle] 초기화 확인 버튼 클릭 완료")
    else:
        log_error("[Battle] 초기화 확인 버튼 미검출")
        
    # 프리셋 캐릭터 클릭 (예시, preset 관련 로직은 본문에 따로 관리)
    # 예: preset_a의 캐릭터 리스트를 순차적으로 클릭
    
    # CURRENT_PRESET에 "A" 또는 "B"가 들어간다고 가정하고, 이를 이용해서 preset 이름 결정
    import global_state
    preset = f"preset_{global_state.CURRENT_PRESET.lower()}" 
    char_list = get_preset_characters(preset)
    if not char_list:
        log_error(f"[Battle] 설정된 preset '{preset}'의 캐릭터 정보가 없습니다.")
    else:
        log_info(f"[Battle] Preset '{preset}'을(를) 이용한 캐릭터 편성 시작")
        for char_img in char_list:
            pos = safe_locate_center(char_img)
            if pos:
                pyautogui.click(pos)
                log_info(f"[Battle] 편성: {char_img} 클릭됨 at {pos}")
                time.sleep(0.2)
            else:
                log_error(f"[Battle] 편성: {char_img} 을(를) 찾지 못함")
    
    # 전투 시작 버튼 클릭
    battle_start_pos = safe_locate_center("images/battle_start_1.png")
    if battle_start_pos:
        pyautogui.click(battle_start_pos)
        log_info("[Battle] 전투 시작 버튼 클릭됨")
    else:
        log_error("[Battle] 전투 시작 버튼 미검출")
    
    # 대략 10초간 로딩 대기 후, 편성이 완료되어 전투 시작
    time.sleep(10)
    log_info("[Battle] 편성 완료 후 전투 시작 준비 완료")

def process_battle():
    """
    전투 진행 루틴:
      - 최초 전투 진입 시 편성 화면이면 formation 과정을 실행.
      - 그 이후에는 전투 대기 상태에서 P키와 Enter키 눌러 턴을 진행.
      - 전투 도중에 선택지 화면이 처리되어 돌아오면, 편성 화면이 나타나지 않고 전투 대기 상태임을 확인.
    """
    global formation_done

    # 먼저 편성 UI(예: 초기화 버튼)가 보이는지 확인
    formation_ui = safe_locate_center("images/reset_button.png")
    if formation_ui and not formation_done:
        log_info("[Battle] 편성 화면 감지됨. 편성 수행 절차 실행")
        run_formation()
        formation_done = True
    else:
        log_error("[Battle] 이미 편성 완료된 상태로 전투 진행. (또는 편성 UI 미검출)")

    
    log_info("[Battle] 전투 진행 루프 시작")
    while True:
        # 전투 대기 화면 감지
        battle_ready_pos = safe_locate_center("images/battle_ready.png")
        if battle_ready_pos:
            log_error("[Battle] 전투 대기 화면: P키와 Enter키 입력 시도")
            
            time.sleep(0.3)
            press_p = safe_locate_center("images/battle_ready.png")
            if press_p:
                pyautogui.click(press_p)
                log_info(f"[select_ego_gift] battle_ready.png 클릭됨 at {press_p}")
            else:
                log_error("[select_ego_gift] battle_ready.png 미검출")
                pyautogui.press('p')

            
            # pyautogui.press('p')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.5)

            # 화면 중앙 좌표로 마우스 이동
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2)
        else:
            log_error("[Battle] 전투 대기 화면 미검출, 현재 상태 점검 중")

        # # 전투 종료 조건1: 보상 팝업 감지
        # battle_reward_popup_pos = safe_locate_center("images/battle_reward_popup.png")
        # if battle_reward_popup_pos:
        #     log_info("[Battle] 전투 완료 보상 팝업 감지됨 via battle_reward_popup.png")
        #     time.sleep(2)
            
        #     import global_state  # 이미 전역 상태 모듈에서 프리셋 정보를 사용합니다.
            
        #     # 현재 프리셋에 따른 보상 이미지 파일명 지정
        #     preset = global_state.CURRENT_PRESET.lower()  # 예: "a"
        #     preset_gift_image = f"images/preset_{preset}_gift.png"
            
        #     log_info(f"[Battle] 보상 이미지 {preset_gift_image} 검색 시작 (3초 대기, confidence=0.5)")
        #     # 3초 동안 preset에 맞는 보상 이미지 검색 (confidence 0.5 적용)
        #     preset_gift_pos = wait_for_image(preset_gift_image, timeout=3, confidence=0.5)
        #     if preset_gift_pos:
        #         pyautogui.click(preset_gift_pos)
        #         log_info(f"[Battle] {preset_gift_image} 클릭됨 at {preset_gift_pos}")
        #     else:
        #         log_error(f"[Battle] {preset_gift_image} 미검출. 기본 get_new_gift.png 검색 시작")
        #         get_new_gift_pos = wait_for_image("images/get_new_gift.png", timeout=3, confidence=0.5)
        #         if get_new_gift_pos:
        #             pyautogui.click(get_new_gift_pos)
        #             log_error(f"[Battle] get_new_gift.png 클릭됨 at {get_new_gift_pos}")
        #         else:
        #             log_error("[Battle] get_new_gift.png도 미검출. battle_reward_popup.png 재시도하여 클릭")
        #             battle_reward_popup_pos2 = safe_locate_center("images/battle_reward_popup.png")
        #             if battle_reward_popup_pos2:
        #                 pyautogui.click(battle_reward_popup_pos2)
        #                 log_info(f"[Battle] battle_reward_popup.png 클릭됨 at {battle_reward_popup_pos2}")
        #             else:
        #                 log_error("[Battle] battle_reward_popup.png도 찾을 수 없음. 다음 단계로 진행합니다.")
            
        #     time.sleep(1)
        #     # start_item_confirm 클릭
        #     start_item_confirm_pos = safe_locate_center("images/start_item_confirm.png")
        #     if start_item_confirm_pos:
        #         pyautogui.click(start_item_confirm_pos)
        #         log_info(f"[Battle] start_item_confirm.png 클릭됨 at {start_item_confirm_pos}")
        #     else:
        #         log_error("[Battle] start_item_confirm.png 미검출")
            
        #     time.sleep(1)
        #     # popup_confirm 클릭
        #     popup_confirm_pos = safe_locate_center("images/popup_confirm.png")
        #     if popup_confirm_pos:
        #         pyautogui.click(popup_confirm_pos)
        #         log_info(f"[Battle] popup_confirm.png 클릭됨 at {popup_confirm_pos}")
        #     else:
        #         log_error("[Battle] popup_confirm.png 미검출")
            
        #     time.sleep(2)
            
        #     # 보스 전투 보상 처리 부분
        #     if global_state.is_boss:
        #         log_info("[Battle] 보스전투 보상 처리 대기 시작 (3초 딜레이)")
        #         time.sleep(3)  # 보스 보상 화면이 안정될 시간을 확보
                
        #         # 프리셋 보상 이미지 파일 이름 동적으로 결정
        #         gift_image = f"images/preset_{global_state.CURRENT_PRESET.lower()}_gift.png"
        #         gift_pos = safe_locate_center(gift_image)
        #         if gift_pos:
        #             pyautogui.click(gift_pos)
        #             log_info(f"[Battle] {gift_image} 클릭됨 at {gift_pos}")
        #         else:
        #             log_error(f"[Battle] {gift_image} 미검출, 기본 get_new_gift.png 탐색 시작")
        #             # get_new_gift.png 이미지가 여러 개 존재할 가능성이 있으므로, 하나라도 찾으면 클릭
        #             new_gift_pos = safe_locate_center("images/get_new_gift.png")
        #             if new_gift_pos:
        #                 pyautogui.click(new_gift_pos)
        #                 log_info(f"[Battle] get_new_gift.png 클릭됨 at {new_gift_pos}")
        #             else:
        #                 log_error("[Battle] get_new_gift.png 미검출, 화면 정중앙 클릭")
        #                 # fallback: 화면 중앙 클릭
        #                 screen_w, screen_h = pyautogui.size()
        #                 center = (screen_w // 2, screen_h // 2)
        #                 pyautogui.click(center)
                
        #         # 보스 보상 처리가 끝나고 stage clear 보상 확인
        #         stage_clear_confirm_pos = safe_locate_center("images/stage_clear_reward_confirm.png")
        #         if stage_clear_confirm_pos:
        #             pyautogui.click(stage_clear_confirm_pos)
        #             log_info(f"[Battle] stage_clear_reward_confirm.png 클릭됨 at {stage_clear_confirm_pos}")
        #         else:
        #             log_error("[Battle] stage_clear_reward_confirm.png 미검출, 화면 정중앙 클릭")
        #             screen_w, screen_h = pyautogui.size()
        #             center = (screen_w // 2, screen_h // 2)
        #             pyautogui.click(center)

        #         # stage_clear_reward_confirm 클릭 후 0.5초 딜레이
        #         time.sleep(0.5)

        #         # battle_reward.png (다시 등장하는 전투 보상 이미지) 탐색 및 클릭
        #         battle_reward_pos = safe_locate_center("images/battle_reward.png")
        #         if battle_reward_pos:
        #             pyautogui.click(battle_reward_pos)
        #             log_info(f"[Battle] battle_reward.png 클릭됨 at {battle_reward_pos}")
        #         else:
        #             log_error("[Battle] battle_reward.png 미검출, 화면 정중앙 클릭")
        #             screen_w, screen_h = pyautogui.size()
        #             center = (screen_w // 2, screen_h // 2)
        #             pyautogui.click(center)

        #         # 추가로 2초 딜레이 후 처리를 마무리함.
        #         time.sleep(2)
                
        #         log_info("[Battle] 보스 전투가 종료되어 보스 보상 처리가 완료됨")
        #         global_state.is_boss = False  # 보스 상태 리셋
        #         formation_done = False
        #         break

        # 전투 종료 조건2: 지도 화면(내 캐릭터) 감지 → 전투 종료
        character_pos = safe_locate_center("images/character.png")
        if character_pos:
            log_info("[Battle] 지도 화면 감지됨. 전투 종료.")
            formation_done = False
            break

        choice_pos = safe_locate_center("images/choice_skip.png")
        if choice_pos:
            log_info("[Battle] 선택지 화면 감지 됨. 전투 로직 일시중단")
            formation_done = False
            break

        card_pos = safe_locate_center("images/card_reward.png")
        if card_pos:
            log_info("[Battle] 카드 보상 화면 감지 됨. 전투 로직 일시중단")
            formation_done = False
            break

        ego_reward_pos = safe_locate_center("images/battle_reward_popup.png")
        if ego_reward_pos:
            log_info("[Battle] 전투 보상 화면 감지 됨. 전투 로직 중단")
            formation_done = False
            break

        result_screen_pos = safe_locate_center("images/result_screen.png")
        if result_screen_pos:
            log_info("[Battle] 컨텐츠 완료 화면 감지 됨. 전투 로직 중단")
            formation_done = False
            break


        # 전투 도중에 선택지 화면이 발생할 수도 있음 → 화면 감지는 automation.py (또는 screen_detector)가 담당
        # 만약 선택지 처리 후 돌아왔다면, formation UI는 없으므로 formation_done가 True 상태로 유지됨
        
        log_warning("[Battle] 전투 진행 중... 대기")
        time.sleep(1)
