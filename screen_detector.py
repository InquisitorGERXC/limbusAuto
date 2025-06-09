# actions/screen_detector.py
import cv2
import numpy as np
import pyautogui
from utils.logger import log_error

def match_template(screen_img, template_path, threshold=0.7):
    """
    주어진 screen_img(컬러 이미지)를 그레이스케일로 변환한 후,
    지정된 템플릿 이미지(template_path)를 사용해 template matching을 수행.
    매칭 점수가 threshold 이상이면 True를 반환.
    """
    try:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise Exception(f"템플릿 이미지 로드 실패: {template_path}")
        
        # screen_img를 그레이스케일로 변환합니다.
        screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= threshold
    except Exception as e:
        log_error("템플릿 매칭 오류: " + str(e))
        return False

def match_template_list(screen_img, template_list, threshold=0.7):
    """
    템플릿 이미지 리스트를 순회하며, 하나라도 매칭되면 True를 반환합니다.
    """
    for template_path in template_list:
        if match_template(screen_img, template_path, threshold):
            return True
    return False

def get_current_state():
    """
    화면 전체를 캡처한 후, 템플릿 매칭을 통해 현재 화면 상태를 판별합니다.
    
    우선순위(높은 것부터):
      1. result: 결과 화면 (예: 전투 결과)
      2. theme_select: 테마 선택 화면
      3. battle_ready: 전투 준비(편성) 화면 – 전투 진행 전, 로딩 후 나타남
      4. battle: 전투 액션 화면 (UI 가려지는 등으로 전투 중인 상태)
      5. map_selection: 지도 화면 (내 캐릭터 아이콘 등)
      6. shop: 상점 화면
      7. choice: 선택지 화면
    
    어느 템플릿도 감지되지 않으면 "unknown"을 반환합니다.
    """
    try:
        # 화면 캡쳐
        screenshot = pyautogui.screenshot()
        # pyautogui는 RGB로 캡쳐하므로 BGR로 변환합니다.
        screen_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # 우선순위 순으로 템플릿 매칭 수행
        if match_template(screen_img, "images/result_screen.png", threshold=0.7):
            return "result"
        elif match_template(screen_img, "images/theme_select.png", threshold=0.7):
            return "theme_select"
        elif match_template(screen_img, "images/battle_ready.png", threshold=0.7):
            return "battle_ready"
        elif match_template(screen_img, "images/battle_screen.png", threshold=0.7):
            return "battle_ready"
        
        elif match_template_list(screen_img, [
                "images/character.png",
                "images/character_1.png",
                "images/character_2.png"
            ], threshold=0.7):
            return "map_selection"
        
        elif match_template(screen_img, "images/card_reward.png", threshold=0.7):
            return "card_reward"
        elif match_template(screen_img, "images/battle_reward_popup.png", threshold=0.7):
            return "battle_ego_reward"
        
        elif match_template(screen_img, "images/get_ego_gift.png", threshold=0.7):
            return "get_ego_gift"
        
        elif match_template(screen_img, "images/shop.png", threshold=0.7):
            return "shop"
        elif match_template(screen_img, "images/choice_skip.png", threshold=0.7):
            return "choice"
        
        else:
            return "unknown"
    except Exception as e:
        log_error("화면 감지 오류: " + str(e))
        return "unknown"
