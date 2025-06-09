# actions/initial_sequence.py
import time
from utils.image_tools import click_image, click_multiple
import pyautogui
from utils.logger import log_error

def startup_sequence(preset):
    # 메인화면: 운전석 클릭
    if not click_image("images/driver_seat.png"):
        log_error("driver_seat 버튼을 찾지 못했습니다. 이미 클릭된 상태일 수 있으므로 건너뜁니다.")
    time.sleep(1)
    
    # 거울 던전 클릭
    if not click_image("images/dungeon.png"):
        log_error("dungeon 버튼을 찾지 못했습니다. 이미 진행된 상태일 수 있으므로 건너뜁니다.")
    time.sleep(1)
    
    # 입장 버튼 및 확인(팝업) 처리
    if not click_image("images/entrance.png"):
        log_error("entrance 버튼이 보이지 않습니다. 건너뜁니다.")
    time.sleep(0.5)
    if not click_image("images/popup_entrance.png"):
        log_error("popup_entrance 버튼이 보이지 않습니다. 건너뜁니다.")
    time.sleep(2)
    
    # 캐릭터 조합 프리셋 선택 (프리셋 이미지)
    # preset이 "A"인 경우 파일명은 preset_a.png로 찾아야 하므로 preset.lower() 사용
    if not click_image(f"images/preset_{preset.lower()}.png"):
        log_error(f"preset_{preset.lower()} 이미지가 보이지 않습니다. 이미 선택된 상태로 간주합니다.")
    if not click_image("images/confirm.png"):
        log_error("confirm 버튼을 찾지 못했습니다. 건너뜁니다.")
    time.sleep(1)
    
    # '가호' 선택 (추후 로직 추가 가능)
    if not click_image("images/selection_option_2.png"):
        log_error("selection_option_2 이미지를 찾지 못했습니다. 건너뜁니다.")
    if not click_image("images/selection_option_3.png"):
        log_error("selection_option_3 이미지를 찾지 못했습니다. 건너뜁니다.")
    time.sleep(1)
    if not click_image("images/option_entrance.png"):
        log_error("option_entrance 버튼을 찾지 못했습니다. 건너뜁니다.")
    time.sleep(1)
    if not click_image("images/popup_confirm.png"):
        log_error("option_entrance 버튼을 찾지 못했습니다. 건너뜁니다.")
    time.sleep(1)
    
    # 시작 아이템 선택 – 프리셋 A 예시
    import global_state
    preset_letter = global_state.CURRENT_PRESET.lower()
    
    # 프리셋별 이미지 파일명을 동적으로 생성
    theme_image       = f"images/start_item_theme_{preset_letter}.png"
    item1_image       = f"images/item1_{preset_letter}.png"
    item2_image       = f"images/item2_{preset_letter}.png"
    item3_image       = f"images/item3_{preset_letter}.png"
    start_confirm_img = "images/start_item_confirm.png"  # 공통 이미지라 가정
    
    # 시작 아이템 선택 – 프리셋에 따른 처리
    if not click_image(theme_image):
        log_error(f"{theme_image} 이미지가 보이지 않습니다. 이미 진행된 단계로 간주합니다.")
    time.sleep(0.5)
    if not click_image(item1_image):
        log_error(f"{item1_image} 이미지를 찾지 못했습니다. 건너뜁니다.")
    if not click_image(item2_image):
        log_error(f"{item2_image} 이미지를 찾지 못했습니다. 건너뜁니다.")
    if not click_image(item3_image):
        log_error(f"{item3_image} 이미지를 찾지 못했습니다. 건너뜁니다.")
    if not click_image(start_confirm_img):
        log_error(f"{start_confirm_img} 버튼을 찾지 못했습니다. 건너뜁니다.")
    
    global_state.initial_phase_done = True
    for _ in range(3):
        pyautogui.click()  # 현재 커서 위치를 클릭
        time.sleep(0.5)
