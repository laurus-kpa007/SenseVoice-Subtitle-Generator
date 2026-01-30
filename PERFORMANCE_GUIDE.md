# 성능 최적화 가이드

## 하드웨어 사양
- **CPU**: Intel Ultra 9 286K (NPU 내장)
- **GPU**: NVIDIA RTX 5070 Ti
- **권장**: GPU 가속 사용

## GPU 가속 설정 (권장)

### 1. CUDA 지원 PyTorch 설치

**방법 1: 자동 설치 스크립트 실행**
```batch
install_gpu.bat
```

**방법 2: 수동 설치**
```batch
pip uninstall torch torchaudio -y
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 2. 확인
프로그램 실행 시 다음 메시지가 표시되어야 합니다:
```
🚀 GPU 사용: NVIDIA GeForce RTX 5070 Ti
   CUDA 버전: 12.1
   GPU 메모리: 16.0GB
```

### 3. 성능 향상
- **CPU 모드**: 약 0.5x ~ 1x 실시간 처리 속도
- **GPU 모드**: 약 5x ~ 15x 실시간 처리 속도
- **예시**: 10분 영상 → GPU: 40초 / CPU: 10분

## NPU 가속 설정 (실험적)

Intel Core Ultra NPU는 경량 AI 작업에 최적화되어 있습니다.

### 설치 (선택사항)
```batch
install_npu.bat
```

**주의**:
- NPU 지원은 실험적이며 FunASR가 완벽히 지원하지 않을 수 있습니다
- GPU가 있다면 GPU 사용을 권장합니다

## 배치 처리 최적화

코드가 자동으로 하드웨어에 맞게 배치 크기를 조정합니다:
- **GPU 모드**: 배치 크기 8 (동시에 8개 세그먼트 처리)
- **CPU 모드**: 배치 크기 1 (순차 처리)

## 메모리 최적화

### GPU 메모리 부족 시
audio_processor.py 파일에서 배치 크기 조정:
```python
batch_size = 4 if device.startswith("cuda") else 1  # 8 → 4로 변경
```

### 시스템 RAM 부족 시
긴 영상을 작은 파일로 분할하거나 VAD 설정을 조정하세요.

## 성능 비교표

| 하드웨어 | 1분 영상 처리 시간 | 1시간 영상 처리 시간 | 배치 크기 |
|---------|------------------|-------------------|----------|
| CPU only | ~60초 | ~60분 | 1 |
| RTX 5070 Ti | ~4초 | ~4분 | 8 |
| 이론상 NPU | ~20초 | ~20분 | 2-4 |

## 트러블슈팅

### CUDA 오류 발생 시
```
CUDA error: no kernel image is available for execution
```
**해결**: PyTorch CUDA 버전 재설치
```batch
install_gpu.bat
```

### GPU 메모리 부족
```
CUDA out of memory
```
**해결**: 배치 크기 줄이기 (위 "메모리 최적화" 참조)

### GPU 사용 안됨
**확인**:
```batch
python -c "import torch; print(torch.cuda.is_available())"
```
- `True`: 정상
- `False`: CUDA 드라이버 또는 PyTorch 재설치 필요

## 추가 최적화 팁

1. **VAD 설정 조정**: 불필요한 침묵 구간 제거
   - `VAD: Strict` → 음성만 처리, 더 빠름

2. **오디오 전처리 비활성화**:
   - MDX 음성 분리 OFF
   - EBU R128 정규화 OFF

3. **SRT vs VTT**:
   - 두 형식의 처리 속도는 동일

4. **다중 파일 처리**:
   - 폴더 단위로 추가하면 순차 자동 처리
