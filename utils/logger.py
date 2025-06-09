# utils/logger.py
import logging
import os

# 로그 파일 이름과 경로 설정
LOG_FILE = "automation_error.log"
LOG_LEVEL = logging.DEBUG  # 전체 로그 레벨 설정 (DEBUG 이상 다 출력됨)

# 로거 생성
logger = logging.getLogger("automation_logger")
logger.setLevel(LOG_LEVEL)

# 포맷터 설정
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 파일 핸들러
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 필요 시 호출할 함수들
def log_debug(message):
    logger.debug(message)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)

def log_critical(message):
    logger.critical(message)
