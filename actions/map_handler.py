# actions/map_handler.py
import time
import math
import pyautogui
from utils.logger import log_error, log_info
import global_state
from utils.confidence_check import get_template_confidence

# ─────────────────────────────
# 설정 값 (필요에 따라 조정)
MIN_CANDIDATE_WIDTH = 50
MIN_CANDIDATE_HEIGHT = 50
CLUSTER_THRESHOLD = 100
# 만약 클러스터링 후 후보가 MAX_VALID_CANDIDATES보다 많으면 해당 카테고리는 빈 영역으로 판단
MAX_VALID_CANDIDATES = 25  
CANDIDATE_CONFIDENCE = 0.55   # 후보 검출 신뢰도 (빈공간 클릭 방지를 위해 높임)
ENTRANCE_CONFIDENCE = 0.6    # 입장 버튼 검출 신뢰도
# ─────────────────────────────


# 카테고리별 템플릿 (우선순위에 따라)
MAP_CANDIDATES = {
    "choice": ["images/map_choice.png", "images/map_choice_2.png", "images/map_choice_3.png"],         # 예: ? 선택지 맵
    "normal": ["images/map_normal_1.png", "images/map_normal_2.png"],   # 일반 전투 맵
    "focus": ["images/map_focus.png", "images/map_focus_2.png"], 
    "hard": ["images/map_hard.png"],
    "shop": ["images/map_shop.png"],
    "boss": ["images/map_boss.png", "images/map_boss_1.png"]
}

PRIORITY_ORDER = ["choice", "normal", "focus", "hard", "shop", "boss"]

def is_map_screen():
    """
    지도 화면 여부 판단:
    플레이어 캐릭터 아이콘 중 하나라도 보이면 지도 화면으로 간주.
    여러 변형 이미지(예: "images/character.png", "images/character_1.png", "images/character_2.png")를 검사합니다.
    """
    templates = [
        "images/character.png",
        "images/character_1.png",
        "images/character_2.png"
    ]
    
    for tpl in templates:
        try:
            pos = pyautogui.locateCenterOnScreen(tpl, confidence=0.5)
            if pos:
                return True
        except Exception as e:
            log_error(f"지도 화면 확인 중 오류 ({tpl}): " + str(e))
    
    return False

def cluster_candidates(candidates, threshold=CLUSTER_THRESHOLD):
    """
    후보 리스트에서, 좌표 간 거리가 threshold 이하이면 동일 후보로 취급하여 클러스터링.
    각 클러스터의 대표 좌표(평균 좌표)를 정수형 좌표로 반환.
    """
    clusters = []
    for candidate in candidates:
        cx, cy, template = candidate
        assigned = False
        for cluster in clusters:
            (qx, qy) = cluster["center"]
            if math.hypot(cx - qx, cy - qy) < threshold:
                cluster["candidates"].append(candidate)
                xs = [c[0] for c in cluster["candidates"]]
                ys = [c[1] for c in cluster["candidates"]]
                cluster["center"] = (sum(xs) / len(xs), sum(ys) / len(ys))
                assigned = True
                break
        if not assigned:
            clusters.append({"center": (cx, cy), "candidates": [candidate]})
    result = []
    for cluster in clusters:
        center = cluster["center"]
        template = cluster["candidates"][0][2]
        result.append((int(center[0]), int(center[1]), template))
    return result

def get_candidates_for_category(category):
    """
    지정한 카테고리의 템플릿을 이용하여 화면에 보이는 후보 영역을 수집.
    - pyautogui.locateAllOnScreen()으로 각 템플릿의 후보를 찾음 (신뢰도 CANDIDATE_CONFIDENCE)
    - 박스 크기가 너무 작으면 (널리 인식될 만한 크기 미만) 배제함.
    - 수집된 후보들을 cluster_candidates()로 클러스터링하여 중복을 제거.
    - 클러스터링 후 후보 수가 MAX_VALID_CANDIDATES보다 많으면 빈 영역으로 판단하여 빈 리스트 반환.
    """
    raw_candidates = []
    templates = MAP_CANDIDATES.get(category, [])
    for template in templates:
        try:
            boxes = list(pyautogui.locateAllOnScreen(template, confidence=CANDIDATE_CONFIDENCE))
            for box in boxes:
                if box.width < MIN_CANDIDATE_WIDTH or box.height < MIN_CANDIDATE_HEIGHT:
                    continue  # 너무 작은 박스는 무시
                cx = box.left + box.width // 2
                cy = box.top + box.height // 2
                raw_candidates.append((cx, cy, template))
                log_info(f"[{category}] 후보 발견: {template} at ({cx}, {cy})")
        except Exception as e:
            log_error(f"이미지 {template} 검출 중 오류: {e}")
    log_info(f"[{category}] 원시 후보 수: {len(raw_candidates)}")
    clustered = cluster_candidates(raw_candidates)
    log_info(f"[{category}] 클러스터링 후 후보 수: {len(clustered)}")
    if len(clustered) > MAX_VALID_CANDIDATES:
        log_info(f"[{category}] 후보 수 {len(clustered)}가 너무 많아 빈 영역으로 판단하여 스킵합니다.")
        return []
    return clustered

def check_for_entrance(timeout=5, delay=0.1, confidence=ENTRANCE_CONFIDENCE, region=None):
    """
    지정한 시간(timeout) 동안 delay 간격마다 "map_entrance.png" (입장 버튼)이 나타나는지 검사.
    발견하면 좌표를 반환, 없으면 None 반환.
    """
    elapsed = 0
    while elapsed < timeout:
        btn = pyautogui.locateCenterOnScreen("images/map_entrance.png", confidence=confidence, region=region)
        if btn:
            return btn
        time.sleep(delay)
        elapsed += delay
    return None

def try_candidates(candidate_list):
    """
    전달받은 후보 리스트(클러스터 대표 좌표)에 대해 순차적으로 클릭하고,
    각 후보 클릭 후 최대 5초 내에 "map_entrance.png"가 나타나는지 검사.
    입장 버튼이 검출되면 해당 버튼을 클릭하고 True 반환.
    """
    for candidate in candidate_list:
        cx, cy, template = candidate
        conf_value = get_template_confidence(template)
        log_info(f"[맵 이동] 후보 시도: {template} at ({cx}, {cy}) - 정확도: {conf_value:.2f}")
        try:
            pyautogui.click(cx, cy)
            time.sleep(0.5)
            entrance = check_for_entrance(timeout=7, delay=0.1)
            if entrance:
                ex, ey = int(entrance[0]), int(entrance[1])
                log_info(f"[맵 이동] 입장 버튼 발견 at ({ex}, {ey}) via {template}. 클릭합니다.")
                pyautogui.click(ex, ey)
                return True
            else:
                log_error(f"[맵 이동] 후보 {template} at ({cx}, {cy}) 실패 (입장 버튼 미검출).")
                time.sleep(0.1)
        except Exception as e:
            log_error(f"[맵 이동] 후보 {template} 처리 중 예외: {e}")
    return False

def try_map_candidates_for_category(category):
    """
    지정한 카테고리 내에서 후보들을 수집(중복 제거 후)하고,
    각 후보를 순차적으로 클릭해 입장 버튼이 나타나는지 시도.
    하나라도 성공하면 True 반환.
    """
    candidates = get_candidates_for_category(category)
    if not candidates:
        log_error(f"[맵 이동] {category} 카테고리 후보 없음 또는 유효하지 않음.")
        return False
    # 오른쪽부터 시작하도록 x 좌표 내림차순 정렬
    candidates = sorted(candidates, key=lambda c: -c[0])
    return try_candidates(candidates)

def process_map():
    """
    지도 처리 메인 함수:
      1. 지도 화면(플레이어 캐릭터 아이콘)이 보이는지 확인.
      2. 전체 맵을 노출시키기 위한 동작:
           (a) 화면 정중앙에서 아래로 1000픽셀 드래그
           (b) 마우스 휠을 두 번 내려 전체 화면 노출
      3. PRIORITY_ORDER 순서대로 각 카테고리에서 후보들을 수집한 후,
         후보들을 순차적으로 클릭하여 (빈 공간이 아닌, 실제 맵 영역만),
         클릭 후 "map_entrance.png"가 나타나면 그 버튼을 클릭하여 입장 진행.
         한 카테고리 내 유효한 후보가 없으면 다음 우선순위로 넘어감.
      4. 모든 카테고리에서 실패하면 "갈 수 있는 맵이 없음"을 로그에 남김.
    """
    

    try:
        if not is_map_screen():
            log_error("현재 지도 화면이 아님.")
            return

        # 전체 맵 노출: 화면 중앙에서 아래로 1000픽셀 드래그 후, 마우스 휠 두 번 내리기
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        pyautogui.moveTo(center_x, center_y)
        pyautogui.mouseDown()
        pyautogui.dragRel(0, 1000, duration=1)
        pyautogui.mouseUp()
        time.sleep(0.8)

        pyautogui.moveTo(center_x, center_y)
        pyautogui.scroll(-500)
        time.sleep(0.8)
        pyautogui.scroll(-500)
        time.sleep(0.8)

        # 우선순위 순으로 각 카테고리의 후보 시도
        for category in PRIORITY_ORDER:
            log_info(f"[맵 이동] 우선순위 시도: {category} 맵")
            if try_map_candidates_for_category(category):
                log_info(f"[맵 이동] {category} 맵 입장 성공!")
                if category == "boss":
                    global_state.is_boss = True
                    log_info("[맵 이동] 보스맵 입장 플래그 설정: is_boss = True")
                return
            else:
                log_info(f"[맵 이동] {category} 맵 후보 모두 실패 또는 유효하지 않음. 다음 카테고리 시도.")
        log_error("모든 맵 후보 시도 실패: 갈 수 있는 맵이 없음.")
    except Exception as e:
        log_error("맵 처리 중 예외 발생: " + str(e))


if __name__ == "__main__":
    from utils.logger import init_logger
    init_logger()  # 로그 초기화 (필요하다면)

    print("지도 탐색 시작 (테스트 실행)")
    process_map()
