# SenseVoice 자막 생성기

[English](README_EN.md)

SenseVoice(FunASR)를 사용하여 동영상 파일에서 자동으로 자막을 생성하는 GUI 프로그램입니다.

Whisper와 달리 SenseVoice는 GPU 없이 **CPU만으로도 최대 27배 실시간 속도**로 자막을 생성합니다. 2시간 30분 영상을 약 5분 만에 처리할 수 있습니다.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)

## 주요 기능

- **초고속 처리** - Whisper 대비 압도적 속도, CPU만으로 최대 27x realtime (2시간 30분 영상 → 약 5분)
- **자동 자막 생성** - MP4, AVI, MKV, MOV, FLV, WMV, WEBM, M4V 등 다양한 동영상 형식 지원
- **다국어 지원** - 한국어, 영어, 일본어 등 50개 이상 언어 자동 감지
- **감정 인식** - 음성의 감정(기쁨, 슬픔, 분노 등)을 감지하여 자막에 태그 추가
- **화자 분리** - 여러 화자를 구분하여 자막에 표시
- **SRT/VTT 형식** - 두 가지 자막 형식 지원
- **음성 감지(VAD)** - 4단계 민감도 조절로 정확한 음성 구간 감지
- **MDX 음성 분리** - 배경음악/소음 제거 후 음성만 추출
- **EBU R128 정규화** - 일정한 볼륨으로 정규화하여 인식률 향상
- **배치 처리** - 폴더 단위 일괄 처리 지원
- **멀티스레드 병렬 처리** - CPU 모드에서 다중 스레드를 활용한 고속 처리
- **GPU 가속** - NVIDIA CUDA GPU 사용 시 추가 가속 가능
- **드래그 앤 드롭** - 파일을 끌어다 놓기만 하면 자동 추가
- **이중 언어 UI** - 한국어/영어 인터페이스 전환 지원
- **설정 자동 저장** - 모든 옵션이 자동으로 저장되어 다음 실행 시 유지

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

| 방법 | 실행 |
|------|------|
| .pyw 파일 더블클릭 | `main.pyw` 더블클릭 |
| VBScript 실행 | `SenseVoice.vbs` 더블클릭 |
| 배치 파일 실행 | `run_gui.bat` 실행 |
| Conda 환경 실행 | `start_with_conda.bat` 실행 |
| 바탕화면 바로가기 | `create_shortcut.vbs` 더블클릭 → 바로가기 생성 |

### 명령줄에서 직접 실행 (CMD 창 없음)
```bash
pythonw main.py
```

## 옵션 설명

### 처리 속도 (모델 선택)
| 모드 | 설명 |
|------|------|
| 빠름 (Small) | 가장 빠른 처리, 기본 정확도 |
| 균형 (Medium) | 속도와 정확도의 균형 |
| 고품질 (Turbo) | 높은 정확도 |
| 최고품질 (Large-v3) | 최고 정확도, 느린 처리 |

### 음성 감지(VAD)
| 모드 | 임계값 | 설명 |
|------|--------|------|
| 끄기 (전체) | - | 전체 오디오 처리 |
| 민감 (많이 감지) | 0.3 | 낮은 임계값으로 더 많은 음성 감지 |
| 보통 | 0.5 | 균형잡힌 감지 |
| 엄격 (적게 감지) | 0.7 | 명확한 음성만 감지 |

### 전처리
- **MDX Kim 음성 분리**: 배경음악/소음 제거 (Highpass 85Hz, Lowpass 8000Hz, EQ 1000Hz +3dB)
- **EBU R128 라우드니스 정규화**: -14 LUFS 기준, True Peak -1.0dB 제한

### 출력 형식
- **SRT**: 표준 자막 형식 (`HH:MM:SS,mmm`)
- **VTT**: WebVTT 형식 (`HH:MM:SS.mmm`), CSS 스타일링 지원

### 부가 기능
- **감정 인식**: 자막에 `[감정] 텍스트` 형태로 감정 태그 추가
- **화자 분리**: SRT에서 `<화자> 텍스트`, VTT에서 `<v 화자>텍스트</v>` 형식
- **타임스탬프 표시**: 자막에 순번 표시

## 출력 파일

- 자막 파일: `원본파일명.srt` 또는 `원본파일명.vtt` (원본과 같은 폴더에 저장)
- 로그 파일: `logs/sensevoice_gui_YYYYMMDD_HHMMSS.log`

## GPU 지원 (선택사항)

### Python 버전 호환성
현재 **Python 3.14**를 사용 중인 경우, PyTorch CUDA 빌드가 아직 제공되지 않아 **CPU 모드로만 작동**합니다.

### GPU 가속 설정 방법

#### 방법 1: Conda 환경 사용 (권장 - 기존 Python 유지)
```bash
# 1. setup_python312_env.bat 실행 (자동 설치)
setup_python312_env.bat

# 2. 이후 실행 시
start_with_conda.bat
```

#### 방법 2: Python 재설치
1. **Python 3.12 다운로드**: https://www.python.org/downloads/
2. **설치 시 "Add Python to PATH" 체크**
3. **패키지 재설치**:
```bash
pip install -r requirements.txt
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -U funasr modelscope python-Levenshtein
```

#### 방법 3: 수동 Conda 환경 생성
```bash
conda create -n sensevoice python=3.12 -y
conda activate sensevoice
pip install -r requirements.txt
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -U funasr modelscope python-Levenshtein
```

### 실측 성능 (CPU, MDX 음성분리 ON)

> Whisper는 CPU에서 1x 이하의 실시간 속도가 일반적이지만, SenseVoice는 CPU만으로도 **최대 27x realtime**을 달성합니다.

| 영상 길이 | 처리 시간 | 속도 | 비고 |
|----------|----------|------|------|
| 143분 (2h 23m) | 5분 20초 | **26.8x realtime** | MDX 음성분리 포함 |
| 148분 (2h 28m) | 5분 21초 | **27.8x realtime** | MDX 음성분리 포함 |

**단계별 소요 시간 (평균):**
| 단계 | 소요 시간 | 비율 |
|------|----------|------|
| 오디오 추출 | ~1분 30초 | 28% |
| ASR 음성 인식 | ~3분 50초 | 72% |
| 자막 생성 | <1초 | ~0% |

> 자세한 성능 최적화 정보는 [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md)를 참고하세요.

## 병렬 처리

- **GPU 모드**: 배치 크기 8로 동시에 8개 세그먼트 처리
- **CPU 모드**: 100개 이상 세그먼트 시 멀티스레드 자동 활성화 (CPU 코어의 70% 활용)
- 처리 실패 시 자동으로 개별 처리로 폴백

## 버전 정보

### v1.2 (2026-01-31)
- UI 크기 1.5배 확대 (1350x1200)
- 폰트 크기 2배 확대 (가독성 향상)
- 버튼 높이 통일 및 시작 버튼 강조
- 로그 영역 2배 확대
- 파일 리스트 좌측 정렬 및 전체 표시
- Python 3.14 호환성 (CPU 모드)
- 멀티스레드 병렬 처리 지원
- 무음 실행 옵션 (콘솔 창 없음)
- Conda 환경 자동 설정

### v1.1 (2026-01-24)
- SenseVoice 메타데이터 태그 자동 제거
- VAD 세그먼트 분리 개선 (merge_vad=False)
- sentence_info와 timestamp 필드 모두 지원

## 라이선스

MIT License
