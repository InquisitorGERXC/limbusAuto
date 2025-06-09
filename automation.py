# automation.py
import time
from actions import initial_sequence, battle_handler, map_handler, shop_handler, choice_handler, result_handler
from screen_detector import get_current_state
from utils.logger import log_error, log_info
import traceback
import os
import keyboard

# 플래그 변수: 선택지 화면 처리가 진행 중인지 여부를 저장
is_choice_processing = False

def exit_callback():
    log_error("종료 단축키(ctrl+c)가 눌렸습니다. 프로그램을 강제 종료합니다.")
    os._exit(0)  # 프로세스를 즉시 종료함. 

def run_automation(preset):
    # 단축키 등록: 프로그램이 시작되면 항상 ctrl+c를 감지하여 즉시 종료합니다.
    keyboard.add_hotkey('ctrl+c', exit_callback)
    import global_state  # 지역적으로 import하여 global_state 변수를 업데이트
    global_state.CURRENT_PRESET = preset  # UI에서 선택된 프리셋 (예, "A" 또는 "B")
    
    # ----- 초기 진행(절차지향적) -----
    try:
        initial_sequence.startup_sequence(preset)
    except Exception as e:
        log_error("[Automation] 초기 시퀀스 오류: " + str(e))
        log_error(traceback.format_exc())
    
    # 초기 단계 완료 여부 플래그 추가 (한 번만 초기 단계를 판단하도록)
    import global_state
    global_state.initial_phase_done = False

    # ----- 동적 화면 감지 루프 -----
    while True:
        # 만약 초기 단계가 아직 완료되지 않았다면,
        # 초기 단계 관련 이미지(예: "preset_a.png")가 보이지 않으면 초기 완료로 간주합니다.
        import global_state
        if not global_state.initial_phase_done:
            try:
                # safe_locate_center가 없다면, battle_handler에서 로컬 import 사용
                from actions.battle_handler import safe_locate_center
                preset_status = safe_locate_center("images/preset_a.png", confidence=0.6)
            except Exception as e:
                log_error("[Automation] 초기 단계 확인 중 오류: " + str(e))
                preset_status = None
            if preset_status is None:
                log_info("[Automation] 초기 단계가 완료된 것으로 간주합니다.")
                initial_phase_done = True
                # 초기 단계가 완료된 후 현재 화면 상태를 한 번 확인
                current_state = get_current_state()
                log_info(f"[Automation] 현재 화면 상태: {current_state}")
            else:
                log_info("[Automation] 초기 단계 작업 진행 중... 계속 대기")
                time.sleep(1)
                continue

        try:
            try:
                current_state = get_current_state()
            except Exception as e:
                log_error("[Automation] 상태 감지(get_current_state) 오류: " + str(e))
                log_error(traceback.format_exc())
                time.sleep(1)
                continue

            if current_state == "result":
                log_info("결과 화면 확인 – 던전 종료. 자동화 종료합니다.")
                result_handler.process_result_screen()
                if result_handler.process_result_screen() :
                    log_info("결과화면 process 완료.")
                break

            elif current_state == "theme_select":
                try:
                    from actions.theme_handler import select_theme_pack
                    select_theme_pack()
                except Exception as e:
                    log_error("[Automation] 테마 선택 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "battle_ready":
                try:
                    battle_handler.process_battle()
                except Exception as e:
                    log_error("[Automation] 전투 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "map_selection":
                try:
                    map_handler.process_map()
                except Exception as e:
                    log_error("[Automation] 지도 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "get_ego_gift":
                try:
                    from actions.battle_reward_handler import get_ego_gift
                    get_ego_gift()
                except Exception as e:
                    log_error("[Automation] EGO 기프트 획득 확인 버튼 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "card_reward":
                try:
                    from actions.battle_reward_handler import card_reward
                    card_reward()
                except Exception as e:
                    log_error("[Automation] 카드 보상 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "battle_ego_reward":
                try:
                    from actions.battle_reward_handler import select_ego_gift
                    select_ego_gift()
                except Exception as e:
                    log_error("[Automation] 기프트 전투 보상 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "shop":
                try:
                    shop_handler.process_shop()
                except Exception as e:
                    log_error("[Automation] 상점 처리 오류: " + str(e))
                    log_error(traceback.format_exc())

            elif current_state == "choice":
                global is_choice_processing
                if not is_choice_processing:
                    is_choice_processing = True
                    try:
                        choice_handler.process_choice()
                    except Exception as e:
                        log_error("[Automation] 선택지 처리 오류: " + str(e))
                        log_error(traceback.format_exc())
                    finally:
                        is_choice_processing = False
                else:
                    log_error("[Automation] 이미 선택지 처리가 진행 중입니다.")

            else:
                # 알 수 없는 상태이면 잠시 대기
                time.sleep(0.5)

        except Exception as e:
            log_error("[Automation] 메인 루프 오류: " + str(e))
            log_error(traceback.format_exc())
            time.sleep(1)
