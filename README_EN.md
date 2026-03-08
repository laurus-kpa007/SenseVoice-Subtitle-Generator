# SenseVoice Subtitle Generator

[한국어](README.md)

A GUI application that automatically generates subtitles from video files using SenseVoice (FunASR).

Unlike Whisper, SenseVoice achieves up to **27x realtime speed on CPU alone** — no GPU required. A 2.5-hour video can be processed in about 5 minutes.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)

## Features

- **Ultra-fast Processing** - Up to 27x realtime on CPU alone (2.5h video → ~5 min), far faster than Whisper
- **Automatic Subtitle Generation** - Supports MP4, AVI, MKV, MOV, FLV, WMV, WEBM, M4V and more
- **Multilingual Support** - Auto-detection for 50+ languages including Korean, English, Japanese
- **Emotion Recognition** - Detects emotions (happy, sad, angry, etc.) and tags them in subtitles
- **Speaker Diarization** - Identifies and labels different speakers
- **SRT/VTT Formats** - Supports both subtitle formats
- **Voice Activity Detection (VAD)** - 4-level sensitivity control for accurate speech detection
- **MDX Voice Separation** - Removes background music/noise, extracts voice only
- **EBU R128 Normalization** - Normalizes volume for improved recognition accuracy
- **Batch Processing** - Process entire folders at once
- **Multithreaded Processing** - High-speed parallel processing using multiple CPU threads
- **GPU Acceleration** - Additional acceleration available with NVIDIA CUDA GPU
- **Drag & Drop** - Simply drag files into the window to add them
- **Bilingual UI** - Switch between Korean and English interface
- **Auto-save Settings** - All options are automatically saved and restored

## Installation

### Automatic Installation (Recommended)

#### Windows
```bash
install.bat
```

#### Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

### Important Notes
- **FunASR**: This program uses FunASR (SenseVoice) as its speech recognition engine
- **editdistance workaround**: Works without a C++ compiler by using `python-Levenshtein` as a fallback
- **Auto-patching**: The install script automatically patches FunASR for compatibility

### SenseVoice Model Download
The model is automatically downloaded on first run.

## Usage

### Basic Launch (with console window)
```bash
python main.py
```

### GUI Only (no console window) - Recommended

| Method | How to Run |
|--------|-----------|
| .pyw file | Double-click `main.pyw` |
| VBScript | Double-click `SenseVoice.vbs` |
| Batch file | Run `run_gui.bat` |
| Conda environment | Run `start_with_conda.bat` |
| Desktop shortcut | Double-click `create_shortcut.vbs` to create a shortcut |

### Command Line (no console window)
```bash
pythonw main.py
```

## Options

### Processing Speed (Model Selection)
| Mode | Description |
|------|-------------|
| Fast (Small) | Fastest processing, basic accuracy |
| Balanced (Medium) | Balance between speed and accuracy |
| High Quality (Turbo) | High accuracy |
| Best Quality (Large-v3) | Maximum accuracy, slower processing |

### Voice Activity Detection (VAD)
| Mode | Threshold | Description |
|------|-----------|-------------|
| Off (Full) | - | Processes entire audio |
| Sensitive | 0.3 | Low threshold, detects more speech |
| Normal | 0.5 | Balanced detection |
| Strict | 0.7 | Only detects clear speech |

### Preprocessing
- **MDX Kim Voice Separation**: Removes background music/noise (Highpass 85Hz, Lowpass 8000Hz, EQ 1000Hz +3dB)
- **EBU R128 Loudness Normalization**: Target -14 LUFS, True Peak limit -1.0dB

### Output Formats
- **SRT**: Standard subtitle format (`HH:MM:SS,mmm`)
- **VTT**: WebVTT format (`HH:MM:SS.mmm`), supports CSS styling

### Additional Features
- **Emotion Recognition**: Adds emotion tags as `[emotion] text` in subtitles
- **Speaker Diarization**: SRT uses `<speaker> text`, VTT uses `<v speaker>text</v>`
- **Timestamp Display**: Shows sequential numbering in subtitles

## Output Files

- Subtitle file: `original_filename.srt` or `original_filename.vtt` (saved in the same folder as the source video)
- Log file: `logs/sensevoice_gui_YYYYMMDD_HHMMSS.log`

## GPU Support (Optional)

### Python Version Compatibility
If using **Python 3.14**, PyTorch CUDA builds are not yet available, so it runs in **CPU mode only**.

### GPU Acceleration Setup

#### Method 1: Conda Environment (Recommended - keeps existing Python)
```bash
# 1. Run setup script (auto-install)
setup_python312_env.bat

# 2. Launch afterwards
start_with_conda.bat
```

#### Method 2: Reinstall Python
1. **Download Python 3.12**: https://www.python.org/downloads/
2. **Check "Add Python to PATH" during installation**
3. **Reinstall packages**:
```bash
pip install -r requirements.txt
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -U funasr modelscope python-Levenshtein
```

#### Method 3: Manual Conda Environment
```bash
conda create -n sensevoice python=3.12 -y
conda activate sensevoice
pip install -r requirements.txt
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -U funasr modelscope python-Levenshtein
```

### Measured Performance (CPU, MDX Voice Separation ON)

> Whisper typically runs at 1x or slower on CPU. SenseVoice achieves up to **27x realtime on CPU alone**.

| Video Duration | Processing Time | Speed | Notes |
|---------------|----------------|-------|-------|
| 143 min (2h 23m) | 5 min 20s | **26.8x realtime** | With MDX voice separation |
| 148 min (2h 28m) | 5 min 21s | **27.8x realtime** | With MDX voice separation |

**Per-stage Breakdown (average):**
| Stage | Time | Ratio |
|-------|------|-------|
| Audio extraction | ~1 min 30s | 28% |
| ASR inference | ~3 min 50s | 72% |
| Subtitle generation | <1s | ~0% |

> For detailed performance tuning, see [PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md).

## Parallel Processing

- **GPU mode**: Batch size 8, processes 8 segments simultaneously
- **CPU mode**: Auto-enables multithreading for 100+ segments (uses 70% of CPU cores)
- Automatic fallback to sequential processing on failure

## Version History

### v1.2 (2026-01-31)
- UI scaled 1.5x larger (1350x1200)
- Font sizes doubled for readability
- Unified button heights with emphasized Start button
- Log area doubled in size
- File list left-aligned with full display
- Python 3.14 compatibility (CPU mode)
- Multithreaded parallel processing support
- Silent launch options (no console window)
- Conda environment auto-setup

### v1.1 (2026-01-24)
- Automatic SenseVoice metadata tag removal
- Improved VAD segment separation (merge_vad=False)
- Support for both sentence_info and timestamp output fields

## License

MIT License
