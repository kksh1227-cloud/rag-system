# Streamlit Cloud용 메인 앱 파일
import sys
import os

# 프론트엔드 경로를 시스템 패스에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend'))

# 메인 앱 실행
from frontend.app import *