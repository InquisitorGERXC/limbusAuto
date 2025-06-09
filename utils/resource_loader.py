### utils/resource_loader.py 
### 필요하다면 가져다 사용. 파일이 하나로 합쳐질 경우 사용
import os
import sys

def resource_path(relative_path):
    """PyInstaller 빌드 후에도 리소스 경로를 정확하게 잡아주는 함수"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
