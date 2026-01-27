#!/bin/bash

echo "SenseVoice 자막 생성기 실행 중..."
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[오류] 프로그램 실행 중 오류가 발생했습니다."
    echo "먼저 ./install.sh를 실행하여 필요한 패키지를 설치해주세요."
fi
