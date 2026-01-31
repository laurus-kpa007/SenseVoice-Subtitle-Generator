# SenseVoice 자막 생성기

SenseVoice를 사용하여 MP4 동영상 파일에서 자동으로 자막을 생성하는 GUI 프로그램입니다.

## 주요 기능

- MP4 동영상에서 자동 자막 생성
- 다국어 지원 (한국어, 영어, 일본어, 중국어 등)
- 감정 인식 기능
- 화자 분리 기능
- SRT/VTT 자막 파일 형식 지원
- 음성 감지(VAD) 옵션
- 배치 처리 지원

## 설치 방법

### 자동 설치 (권장)

#### Windows
```bash
install.bat
```

#### Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

### 중요 사항
- **FunASR 설치**: 이 프로그램은 FunASR(SenseVoice)를 사용합니다
- **editdistance 문제 해결**: C++ 컴파일러가 없어도 `python-Levenshtein`으로 대체하여 동작합니다
- **자동 패치**: 설치 스크립트가 자동으로 FunASR을 패치합니다

### SenseVoice 모델 다운로드
처음 실행 시 자동으로 모델이 다운로드됩니다.

## 사용 방법

### 기본 실행 (CMD 창 표시됨)
```bash
python main.py
```

### GUI만 실행 (CMD 창 숨김) - 권장

**방법 1: .pyw 파일 더블클릭**
```
main.pyw 파일을 더블클릭
```

**방법 2: VBScript 실행**
```
SenseVoice.vbs 파일을 더블클릭
```

**방법 3: 배치 파일 실행**
```
run_gui.bat 실행
```

**방법 4: 바탕화면 바로가기 생성**
```
create_shortcut.vbs 파일을 더블클릭
→ 바탕화면에 "SenseVoice 자막 생성기" 바로가기 생성됨
```

### 명령줄에서 직접 실행 (CMD 창 없음)
```bash
pythonw main.py
```

## 옵션 설명

### 처리 속도
- **빠름 (Small)**: 가장 빠른 처리, 기본 정확도
- **균형 (Medium)**: 속도와 정확도의 균형
- **고품질 (Turbo)**: 높은 정확도
- **최고품질 (Large-v3)**: 최고 정확도, 느린 처리

### 음성 감지(VAD)
- **끄기 (전체)**: 전체 오디오 처리
- **만감 (많이 감지)**: 낮은 임계값으로 더 많은 음성 감지
- **보통**: 균형잡힌 감지
- **엄격 (적게 감지)**: 높은 임계값으로 명확한 음성만 감지

### 전처리
- **MDX Kim 음성 분리**: 배경음악/소음 제거하고 음성만 추출

### 음향 정규화
- **EBU R128 라우드니스 정규화**: 일정한 볼륨으로 정규화하여 인식률 향상

### 언어 선택
- 일본어, 영어, 한국어 등 지원
- 자동 감지 가능

## 출력 파일

- 자막 파일: `원본파일명.srt` 또는 `원본파일명.vtt`
- 로그 파일: `logs/sensevoice_gui_YYYYMMDD_HHMMSS.log`

## GPU 지원 (선택사항)

### 중요: Python 버전 호환성
현재 **Python 3.14**를 사용 중인 경우, PyTorch CUDA 빌드가 아직 제공되지 않아 **CPU 모드로만 작동**합니다.

### GPU 가속 설정 방법

#### 방법 1: Conda 환경 사용 (권장 - 기존 Python 유지)
```bash
# 1. setup_python312_env.bat 실행 (자동 설치)
setup_python312_env.bat

# 2. 이후 실행 시
run_sensevoice.bat
```

#### 방법 2: Python 재설치
1. **Python 3.12 다운로드**: https://www.python.org/downloads/
2. **설치 시 "Add Python to PATH" 체크** ✓
3. **패키지 재설치**:
```bash
cd d:\Python\SenseVoice
pip install -r requirements.txt
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -U funasr modelscope python-Levenshtein
```

#### 방법 3: 수동 Conda 환경 생성
```bash
conda create -n sensevoice python=3.12 -y
conda activate sensevoice
cd d:\Python\SenseVoice
pip install -r requirements.txt
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -U funasr modelscope python-Levenshtein
```

### 현재 환경 (Python 3.14)
- ✅ CPU 모드로 정상 작동
- ⚠️ GPU 가속은 Python 3.12 환경 필요
- ⏱️ 처리 속도: CPU 모드 (약 1x 실시간) vs GPU 모드 (약 15x 실시간)

## 버전 정보

### v1.2 (2026-01-31)
- UI 크기 1.5배 확대 (1350x1200)
- 폰트 크기 2배 확대 (가독성 향상)
- 버튼 높이 통일 및 시작 버튼 강조
- 로그 영역 2배 확대
- 파일 리스트 좌측 정렬 및 전체 표시
- Python 3.14 호환성 (CPU 모드)

### v1.1 (2026-01-24)
- SenseVoice 메타데이터 태그 자동 제거
  - `<|언어|>`, `<|감정|>`, `<|Speech|>` 등의 태그가 자막에 포함되지 않음
  - `<speaker_N>` 화자 태그 자동 정제
- VAD 세그먼트 분리 개선
  - merge_vad=False로 변경하여 타임스탬프 정확도 향상
  - 세그먼트별 정확한 타이밍 정보 유지
- sentence_info와 timestamp 필드 모두 지원
  - FunASR의 다양한 출력 형식 호환

## 라이선스

MIT License
