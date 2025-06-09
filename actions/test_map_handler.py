# actions/test_map_handler.py
import sys
import os
# 프로젝트 루트 디렉터리 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
from actions.map_handler import (
    is_map_screen, 
    find_candidate_nodes, 
    sort_candidates, 
    select_map_candidate, 
    process_map
)

def test_is_map_screen():
    print("== 지도 화면 판별 테스트 ==")
    if is_map_screen():
        print("▶ 지도 화면이 감지되었습니다.")
    else:
        print("▶ 지도 화면이 감지되지 않았습니다.")

def test_find_candidates():
    print("\n== 후보 노드 탐색 테스트 ==")
    candidates = find_candidate_nodes()
    if candidates:
        print("▶ 후보 노드들이 발견되었습니다:")
        for candidate in candidates:
            # candidate는 (category, 위치, 템플릿 파일명) 튜플입니다.
            print("   -", candidate)
    else:
        print("▶ 후보 노드가 발견되지 않았습니다.")

def test_sort_candidates():
    print("\n== 후보 노드 정렬 테스트 ==")
    candidates = find_candidate_nodes()
    sorted_candidates = sort_candidates(candidates)
    if sorted_candidates:
        print("▶ 정렬된 후보 노드 리스트:")
        for candidate in sorted_candidates:
            print("   -", candidate)
    else:
        print("▶ 정렬할 후보 노드가 없습니다.")

def test_select_map_candidate():
    print("\n== 맵 후보 노드 선택 테스트 ==")
    result = select_map_candidate()
    if result:
        print("▶ 지도 이동: 후보 노드를 통해 입장 버튼 발견 및 클릭 성공!")
    else:
        print("▶ 지도 이동: 유효한 경로를 선택하지 못했습니다.")

def test_process_map():
    print("\n== 전체 지도 처리 테스트 ==")
    process_map()
    # process_map 내부에서 로그 출력이나 실행 결과를 남기므로, 시험 후 결과 로그를 확인하세요.

def run_all_tests():
    print(">>>> 지도 핸들러 테스트 시작 <<<<")
    test_is_map_screen()
    time.sleep(1)
    test_find_candidates()
    time.sleep(1)
    test_sort_candidates()
    time.sleep(1)
    test_select_map_candidate()
    time.sleep(1)
    test_process_map()
    print("\n>>>> 지도 핸들러 테스트 완료 <<<<")

if __name__ == '__main__':
    run_all_tests()
