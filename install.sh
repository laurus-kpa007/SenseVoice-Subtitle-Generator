#!/bin/bash

echo "========================================"
echo "SenseVoice 자막 생성기 설치 스크립트"
echo "========================================"
echo ""

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "[오류] Python3가 설치되어 있지 않습니다."
    echo "Python 3.8 이상을 설치해주세요."
    exit 1
fi

echo "[1/4] Python 패키지 설치 중..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[오류] 패키지 설치 실패"
    exit 1
fi

echo ""
echo "[2/4] FFmpeg 확인 중..."
if ! command -v ffmpeg &> /dev/null; then
    echo "[경고] FFmpeg가 설치되어 있지 않습니다."
    echo "FFmpeg를 설치해주세요:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo ""
else
    echo "[확인] FFmpeg가 정상적으로 설치되어 있습니다."
fi

echo ""
echo "[3/4] 디렉토리 구조 생성 중..."
mkdir -p logs
mkdir -p temp

echo ""
echo "[4/4] CUDA 확인 중..."
python3 -c "import torch; print('CUDA 사용 가능:', torch.cuda.is_available())" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "[경고] PyTorch가 올바르게 설치되지 않았습니다."
    echo "CPU 모드로 실행됩니다. (속도가 느릴 수 있습니다)"
    echo ""
    echo "CUDA 가속을 사용하려면 다음 명령어로 PyTorch를 재설치하세요:"
    echo "pip3 uninstall torch torchaudio"
    echo "pip3 install torch torchaudio --index-url https://download.pytorch.org/whl/cu118"
fi

echo ""
echo "========================================"
echo "설치가 완료되었습니다!"
echo "========================================"
echo ""
echo "프로그램을 실행하려면 다음 명령어를 입력하세요:"
echo "  ./run.sh"
echo "또는"
echo "  python3 main.py"
echo ""

# 실행 권한 부여
chmod +x run.sh
