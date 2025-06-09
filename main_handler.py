# actions/main_handler.py
import time
from screen_detector import get_current_state
from actions.battle_handler import process_battle
from actions.choice_handler import process_choice

def main_loop():
    """
    메인 루프:
      - 주기적으로 화면 상태를 get_current_state() 함수를 통해 판별합니다.
      - 반환된 상태 값에 따라 전투 혹은 선택지 처리 핸들러를 호출합니다.
      
      예:
        - 전투 준비 상태나 전투 액션 상태: "battle_ready", "battle", "battle_screen" → process_battle() 호출
        - 선택지 상태: "choice" → process_choice() 호출
        - 그 외: 일정 시간 대기 후 상태 재확인
    """
    while True:
        state = get_current_state()
        if state in ["battle_ready", "battle", "battle_screen"]:
            # 전투 관련 상태이면 전투 핸들러 호출
            process_battle()
        elif state == "choice":
            # 선택지 화면이면 선택지 핸들러 호출
            process_choice()
        else:
            # 기타 상태(예: map_selection, shop 등)에는 별도 처리 또는 단순 대기
            time.sleep(1)

if __name__ == "__main__":
    main_loop()
