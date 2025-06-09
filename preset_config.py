# 각 preset별 편성 캐릭터 이미지 목록
PRESET_DATA = {
    "preset_a": ["images/char_heishou_faust.png", "images/char_heishou_ryoshu.png", "images/char_family_ishmael.png", "images/char_heishou_rodion.png",
                 "images/char_heishou_outis.png", "images/char_heishou_gregor.png", "images/char_fanghunt_honglu.png"],
                 
    "preset_b": ["images/character_M.png", "images/character_N.png", "images/character_O.png", "images/character_P.png",
                 "images/character_Q.png", "images/character_R.png", "images/character_S.png", "images/character_T.png",
                 "images/character_U.png", "images/character_V.png", "images/character_W.png", "images/character_X.png"],

    # 미래에 추가될 가능성이 있는 preset_c (초기 설정 없음)
    "preset_c": []
}

def get_preset_characters(preset_name):
    """ 지정한 preset에 맞는 캐릭터 리스트를 반환 """
    return PRESET_DATA.get(preset_name, [])
