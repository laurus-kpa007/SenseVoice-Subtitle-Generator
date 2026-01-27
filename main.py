#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SenseVoice 자막 생성기 메인 실행 파일

MP4 동영상 파일에서 자동으로 자막을 생성하는 GUI 프로그램입니다.
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == '__main__':
    main()
