import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QRadioButton, QCheckBox,
                             QPushButton, QTextEdit, QButtonGroup, QFileDialog,
                             QMessageBox, QProgressBar, QFrame, QComboBox,
                             QGraphicsDropShadowEffect, QSplitter, QGroupBox,
                             QListWidget, QAbstractItemView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QFont, QTextCursor, QColor, QPalette, QLinearGradient, QBrush, QIcon
import json


# ==================== Internationalization ====================
TRANSLATIONS = {
    'ko': {
        'window_title': 'SenseVoice 자막 생성기',
        'drop_area': '파일을 드래그해주세요.',
        'drop_area_or': '또는',
        'processing_speed': '처리 속도',
        'fast': '빠름',
        'balanced': '균형',
        'high_quality': '고품질',
        'best_quality': '최고품질',
        'recommended': '권장',
        'voice_detection': '음성 감지 (VAD)',
        'off': '끄기',
        'sensitive': '민감',
        'normal': '보통',
        'strict': '엄격',
        'preprocessing': '전처리 옵션',
        'mdx_separation': 'MDX 음성 분리',
        'mdx_desc': '배경음 제거로 인식률 향상',
        'normalize': '음량 정규화',
        'normalize_desc': '작은 소리 증폭 (EBU R128)',
        'transcription_lang': '인식 언어',
        'korean': '한국어',
        'english': '영어',
        'japanese': '일본어',
        'additional_features': '추가 기능',
        'emotion': '감정 인식',
        'speaker': '화자 분리',
        'timestamp': '타임스탬프',
        'subtitle_format': '자막 형식',
        'add_files': '파일 추가',
        'add_folder': '폴더 추가',
        'clear_list': '목록 초기화',
        'cancel': '취소',
        'start': '시작',
        'exit': '종료',
        'ready': '준비됨',
        'processing': '처리 중...',
        'completed': '완료',
        'error': '오류 발생',
        'log': '실행 로그',
        'files_selected': '개 파일 선택됨',
        'and_more': '외',
        'more_files': '개',
        'warning': '경고',
        'no_video_files': '지원하는 동영상 파일이 없습니다.',
        'select_video': '처리할 동영상 파일을 선택해주세요.',
        'processing_start': '처리 시작',
        'audio_extract': '오디오 추출 중...',
        'speech_recognition': '음성 인식 중...',
        'subtitle_generation': '자막 생성 중...',
        'complete': '완료',
        'all_complete': '모든 파일 처리가 완료되었습니다.',
        'cancelled': '처리가 취소되었습니다.',
        'ui_language': 'UI 언어',
    },
    'en': {
        'window_title': 'SenseVoice Subtitle Generator',
        'drop_area': 'Drag and drop video files here',
        'drop_area_or': 'or',
        'processing_speed': 'Processing Speed',
        'fast': 'Fast',
        'balanced': 'Balanced',
        'high_quality': 'High Quality',
        'best_quality': 'Best Quality',
        'recommended': 'Recommended',
        'voice_detection': 'Voice Detection (VAD)',
        'off': 'Off',
        'sensitive': 'Sensitive',
        'normal': 'Normal',
        'strict': 'Strict',
        'preprocessing': 'Preprocessing',
        'mdx_separation': 'MDX Voice Separation',
        'mdx_desc': 'Remove background noise for better accuracy',
        'normalize': 'Audio Normalization',
        'normalize_desc': 'Amplify quiet audio (EBU R128)',
        'transcription_lang': 'Recognition Language',
        'korean': 'Korean',
        'english': 'English',
        'japanese': 'Japanese',
        'additional_features': 'Additional Features',
        'emotion': 'Emotion Recognition',
        'speaker': 'Speaker Diarization',
        'timestamp': 'Timestamps',
        'subtitle_format': 'Subtitle Format',
        'add_files': 'Add Files',
        'add_folder': 'Add Folder',
        'clear_list': 'Clear List',
        'cancel': 'Cancel',
        'start': 'Start',
        'exit': 'Exit',
        'ready': 'Ready',
        'processing': 'Processing...',
        'completed': 'Completed',
        'error': 'Error',
        'log': 'Log',
        'files_selected': 'files selected',
        'and_more': 'and',
        'more_files': 'more',
        'warning': 'Warning',
        'no_video_files': 'No supported video files found.',
        'select_video': 'Please select video files to process.',
        'processing_start': 'Processing started',
        'audio_extract': 'Extracting audio...',
        'speech_recognition': 'Recognizing speech...',
        'subtitle_generation': 'Generating subtitles...',
        'complete': 'Complete',
        'all_complete': 'All files have been processed.',
        'cancelled': 'Processing cancelled.',
        'ui_language': 'UI Language',
    }
}


# ==================== Modern Style Sheet (Neutral Dark / Zinc) ====================
MODERN_STYLE = """
QMainWindow {
    background-color: #18181b;  /* Zinc 950 */
}

QWidget {
    color: #f4f4f5;  /* Zinc 100 */
    font-family: 'Pretendard', 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
}

QGroupBox {
    background-color: #27272a;  /* Zinc 900 */
    border: 1px solid #3f3f46;  /* Zinc 700 */
    border-radius: 12px;
    margin-top: 12px;
    padding: 20px 15px 15px 15px;
    font-weight: bold;
    font-size: 16px; 
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    color: #818cf8;  /* Indigo 400 */
    font-weight: bold;
}

QLabel {
    color: #f4f4f5;
    font-size: 14px;
}

QRadioButton {
    color: #a1a1aa;  /* Zinc 400 */
    spacing: 8px;
    font-size: 14px;
    padding: 4px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #52525b;  /* Zinc 600 */
    background-color: #18181b;
}

QRadioButton::indicator:checked {
    background-color: #6366f1;  /* Indigo 500 */
    border-color: #6366f1;
}

QRadioButton::indicator:hover {
    border-color: #818cf8;
}

QCheckBox {
    color: #a1a1aa;
    spacing: 8px;
    font-size: 14px;
    padding: 4px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #52525b;
    background-color: #18181b;
}

QCheckBox::indicator:checked {
    background-color: #6366f1;
    border-color: #6366f1;
}

QCheckBox::indicator:hover {
    border-color: #818cf8;
}

QPushButton {
    background-color: #3f3f46;  /* Zinc 700 */
    color: #f4f4f5;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #52525b;  /* Zinc 600 */
}

QPushButton:pressed {
    background-color: #27272a;
}

QPushButton:disabled {
    background-color: #27272a;
    color: #52525b;
    border: 1px solid #3f3f46;
}

QPushButton#startButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1, stop:1 #8b5cf6);  /* Indigo to Violet */
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 24px;
    border-radius: 10px;
}

QPushButton#startButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #818cf8, stop:1 #a78bfa);
}

QPushButton#startButton:disabled {
    background: #3f3f46;
    color: #71717a;
}

QTextEdit {
    background-color: #27272a;
    color: #e4e4e7;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    selection-background-color: #6366f1;
}

QComboBox {
    background-color: #3f3f46;
    color: #f4f4f5;
    border: 1px solid #52525b;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 14px;
    min-width: 80px;
}

QComboBox:hover {
    border-color: #6366f1;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #818cf8;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #27272a;
    color: #f4f4f5;
    selection-background-color: #6366f1;
    border: 1px solid #52525b;
    border-radius: 6px;
}

QScrollBar:vertical {
    background-color: #27272a;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #52525b;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #71717a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QProgressBar {
    background-color: #27272a;
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1, stop:1 #8b5cf6);
    border-radius: 4px;
}

QListWidget {
    background-color: transparent;
    border: none;
    color: #f4f4f5;
    font-size: 16px;
    outline: none;
}

QListWidget::item {
    padding: 8px;
    border-radius: 6px;
}

QListWidget::item:hover {
    background-color: #3f3f46;
}

QListWidget::item:selected {
    background-color: #52525b;
    color: white;
}
"""


class ProcessThread(QThread):
    """비동기 처리를 위한 스레드"""
    progress_signal = pyqtSignal(str)
    # index: 파일 인덱스, status: 'running', 'done', 'error'
    item_status_signal = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, video_paths, options, lang='ko'):
        super().__init__()
        self.video_paths = video_paths
        self.options = options
        self.lang = lang
        self.t = TRANSLATIONS[lang]

    def run(self):
        """실제 처리 작업 실행"""
        try:
            from audio_processor import AudioProcessor
            from subtitle_generator import SubtitleGenerator
            import traceback

            processor = AudioProcessor(self.options)
            subtitle_gen = SubtitleGenerator(self.options)

            for i, video_path in enumerate(self.video_paths):
                # 시작 상태 전송
                self.item_status_signal.emit(i, 'running')
                
                try:
                    self.progress_signal.emit(f"\n📁 {self.t['processing_start']}: {os.path.basename(video_path)}")

                    self.progress_signal.emit(f"  ⏳ 1/3 - {self.t['audio_extract']}")
                    audio_path = processor.extract_audio(video_path)

                    self.progress_signal.emit(f"  ⏳ 2/3 - {self.t['speech_recognition']}")
                    transcription = processor.transcribe(audio_path)

                    self.progress_signal.emit(f"  ⏳ 3/3 - {self.t['subtitle_generation']}")
                    subtitle_path = subtitle_gen.generate(transcription, video_path)

                    self.progress_signal.emit(f"  ✅ {self.t['complete']}: {subtitle_path}\n")

                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                    
                    # 완료 상태 전송
                    self.item_status_signal.emit(i, 'done')

                except Exception as file_error:
                    error_detail = traceback.format_exc()
                    self.progress_signal.emit(f"\n  ❌ {self.t['error']}: {os.path.basename(video_path)}")
                    self.progress_signal.emit(f"  {str(file_error)}")
                    
                    # 에러 상태 전송
                    self.item_status_signal.emit(i, 'error')
                    continue

            self.finished_signal.emit(True, self.t['all_complete'])

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            self.progress_signal.emit(f"\n❌ {str(e)}")
            self.finished_signal.emit(False, str(e))


class DropArea(QFrame):
    """모던 드래그 앤 드롭 영역 (QListWidget 포함)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_gui = parent
        self.setAcceptDrops(True)
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedHeight(120)
        self.setStyleSheet("""
            DropArea {
                background-color: #18181b;
                border: 2px dashed #71717a;  /* Zinc 500 */
                border-radius: 16px;
            }
            DropArea:hover {
                border-color: #6366f1;
                background-color: #27272a;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(20, 10, 20, 10)

        # 1. 안내 메시지 컨테이너 (아이콘 + 텍스트)
        self.msg_container = QWidget()
        msg_layout = QVBoxLayout(self.msg_container)
        msg_layout.setContentsMargins(0, 0, 0, 0)
        msg_layout.setSpacing(10)

        # 아이콘
        self.icon_label = QLabel("🎬")
        self.icon_label.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        msg_layout.addWidget(self.icon_label)

        # 메인 텍스트
        self.text_label = QLabel()
        self.text_label.setStyleSheet("""
            font-size: 24px;
            color: #f4f4f5;
            background: transparent;
            border: none;
            font-weight: bold;
        """)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        msg_layout.addWidget(self.text_label)

        # 서브 텍스트
        self.sub_label = QLabel()
        self.sub_label.setStyleSheet("""
            font-size: 16px;
            color: #a1a1aa;
            background: transparent;
            border: none;
        """)
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.sub_label.setWordWrap(True)
        msg_layout.addWidget(self.sub_label)

        self.layout.addWidget(self.msg_container)

        # 2. 파일 리스트 위젯 (초기엔 숨김)
        self.file_list_widget = QListWidget()
        self.file_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.file_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.file_list_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.file_list_widget.setFocusPolicy(Qt.NoFocus)
        self.file_list_widget.hide()
        self.layout.addWidget(self.file_list_widget)

    def update_text(self, main_text, sub_text="", icon="🎬"):
        self.icon_label.setText(icon)
        self.text_label.setText(main_text)
        self.sub_label.setText(sub_text)

    def update_files(self, files, header_text=""):
        """파일 목록 업데이트 및 뷰 전환"""
        if not files:
            # 파일이 없으면 안내 메시지 표시
            self.file_list_widget.hide()
            self.msg_container.show()
            self.layout.setAlignment(Qt.AlignCenter)
        else:
            # 파일이 있으면 리스트 위젯 표시
            self.msg_container.hide()
            self.file_list_widget.show()
            # 레이아웃 정렬을 꽉 채우기로 변경 (리스트가 확장되도록)
            self.layout.setAlignment(Qt.AlignJustify) 
            
            self.file_list_widget.clear()
            
            # 헤더 아이템 (선택사항 - 아이콘 대신 텍스트로 표시)
            if header_text:
                self.file_list_widget.addItem(f"📂 {header_text}")

            for i, f in enumerate(files):
                filename = os.path.basename(f)
                self.file_list_widget.addItem(f"{i+1}. {filename}")
                self.set_item_status(i, 'wait') # 초기 상태

    def set_item_status(self, index, status):
        """특정 인덱스의 아이템 상태 업데이트"""
        # 헤더가 있는 경우 인덱스 조정 (헤더가 1개 있으므로 +1)
        # update_files에서 헤더를 추가했으므로 실제 파일 인덱스는 index + 1
        list_index = index + 1 
        
        if list_index >= self.file_list_widget.count():
            return

        item = self.file_list_widget.item(list_index)
        original_text = item.text()
        
        # 이미 상태 아이콘이 있다면 제거하고 순수 파일명만 추출
        if any(x in original_text for x in ['⏳', '✅', '❌']):
            # "번호. 파일명" 형태 유지를 위해
            try:
                parts = original_text.split('. ', 1)
                if len(parts) > 1:
                    base_text = f"{index+1}. {parts[1].strip()}"
                else:
                    base_text = original_text # 예외 처리
            except:
                base_text = original_text
        else:
            base_text = original_text

        if status == 'running':
            item.setText(f"⏳ {base_text}")
            item.setForeground(QColor("#facc15")) # Yellow
        elif status == 'done':
            item.setText(f"✅ {base_text}")
            item.setForeground(QColor("#4ade80")) # Green
        elif status == 'error':
            item.setText(f"❌ {base_text}")
            item.setForeground(QColor("#f87171")) # Red
        else: # wait
            item.setText(base_text)
            item.setForeground(QColor("#f4f4f5")) # 기본색

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet("""
                DropArea {
                    background-color: #27272a;
                    border: 2px solid #6366f1;
                    border-radius: 16px;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            DropArea {
                background-color: #18181b;
                border: 2px dashed #71717a;
                border-radius: 16px;
            }
            DropArea:hover {
                border-color: #6366f1;
                background-color: #27272a;
            }
        """)

    def dropEvent(self, event):
        self.dragLeaveEvent(event)
        if self.parent_gui:
            self.parent_gui.handle_drop(event)


class SenseVoiceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_paths = []
        self.current_lang = 'ko'
        self.t = TRANSLATIONS[self.current_lang]
        self.init_ui()
        self.load_settings()

    def tr(self, key):
        """번역 헬퍼"""
        return self.t.get(key, key)

    def change_language(self, lang_code):
        """UI 언어 변경"""
        self.current_lang = lang_code
        self.t = TRANSLATIONS[lang_code]
        self.update_all_texts()

    def update_all_texts(self):
        """모든 텍스트 업데이트"""
        self.setWindowTitle(self.tr('window_title'))
        
        # Drop area
        if not self.video_paths:
            self.drop_area.update_text(
                self.tr('drop_area'),
                f"{self.tr('drop_area_or')} {self.tr('add_files')} / {self.tr('add_folder')}"
            )
        else:
            self.update_file_list_display()
        
        # Group boxes
        self.speed_group.setTitle(f"⚡ {self.tr('processing_speed')}")
        self.vad_group.setTitle(f"🎤 {self.tr('voice_detection')}")
        self.preprocess_group.setTitle(f"🔧 {self.tr('preprocessing')}")
        self.lang_group_box.setTitle(f"🌐 {self.tr('transcription_lang')}")
        self.extra_group.setTitle(f"✨ {self.tr('additional_features')}")
        self.format_group_box.setTitle(f"📄 {self.tr('subtitle_format')}")
        
        # Speed options
        self.model_small.setText(self.tr('fast'))
        self.model_medium.setText(self.tr('balanced'))
        self.model_turbo.setText(self.tr('high_quality'))
        self.model_large.setText(f"{self.tr('best_quality')} ★")
        
        # VAD options
        self.vad_off.setText(self.tr('off'))
        self.vad_sensitive.setText(self.tr('sensitive'))
        self.vad_normal.setText(self.tr('normal'))
        self.vad_strict.setText(self.tr('strict'))
        
        # Preprocessing
        self.mdx_check.setText(self.tr('mdx_separation'))
        self.normalize_check.setText(self.tr('normalize'))
        
        # Language options
        self.lang_ko.setText(self.tr('korean'))
        self.lang_en.setText(self.tr('english'))
        self.lang_ja.setText(self.tr('japanese'))
        
        # Extra features
        self.emotion_check.setText(self.tr('emotion'))
        self.speaker_check.setText(self.tr('speaker'))
        self.timestamp_check.setText(self.tr('timestamp'))
        
        # Buttons
        self.add_file_btn.setText(f"📄 {self.tr('add_files')}")
        self.add_folder_btn.setText(f"📁 {self.tr('add_folder')}")
        self.clear_btn.setText(f"🗑 {self.tr('clear_list')}")
        self.cancel_btn.setText(self.tr('cancel'))
        self.start_btn.setText(f"▶  {self.tr('start')}")
        self.close_btn.setText(self.tr('exit'))
        
        # Status
        if self.status_label.text() in ['준비됨', 'Ready']:
            self.status_label.setText(self.tr('ready'))
        
        # Log label
        self.log_label.setText(f"📋 {self.tr('log')}")

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(self.tr('window_title'))
        self.setGeometry(100, 100, 1000, 900) # 더 적절한 기본 크기
        self.setStyleSheet(MODERN_STYLE)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # 헤더 (타이틀 + 언어 선택)
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🎬 SenseVoice")
        title_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #f4f4f5;
            background: transparent;
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # UI 언어 선택
        lang_select_layout = QHBoxLayout()
        lang_select_layout.setSpacing(8)
        
        self.ui_lang_label = QLabel(self.tr('ui_language') + ":")
        self.ui_lang_label.setStyleSheet("color: #a1a1aa; font-size: 14px;")
        lang_select_layout.addWidget(self.ui_lang_label)
        
        self.ui_lang_combo = QComboBox()
        self.ui_lang_combo.addItem("한국어", "ko")
        self.ui_lang_combo.addItem("English", "en")
        self.ui_lang_combo.currentIndexChanged.connect(self.on_ui_language_changed)
        lang_select_layout.addWidget(self.ui_lang_combo)
        
        header_layout.addLayout(lang_select_layout)
        main_layout.addLayout(header_layout)

        # 드래그 앤 드롭 영역
        self.drop_area = DropArea(self)
        self.drop_area.update_text(
            self.tr('drop_area'),
            f"{self.tr('drop_area_or')} {self.tr('add_files')} / {self.tr('add_folder')}"
        )
        main_layout.addWidget(self.drop_area)

        # 옵션 영역 (2열 그리드)
        options_layout = QHBoxLayout()
        options_layout.setSpacing(16)
        
        # 왼쪽 열
        left_col = QVBoxLayout()
        left_col.setSpacing(12)
        
        # 처리 속도
        self.speed_group = QGroupBox(f"⚡ {self.tr('processing_speed')}")
        speed_layout = QVBoxLayout()
        speed_layout.setSpacing(4)
        
        self.model_group = QButtonGroup()
        self.model_small = QRadioButton(self.tr('fast'))
        self.model_medium = QRadioButton(self.tr('balanced'))
        self.model_turbo = QRadioButton(self.tr('high_quality'))
        self.model_large = QRadioButton(f"{self.tr('best_quality')} ★")
        self.model_large.setChecked(True)
        
        self.model_group.addButton(self.model_small, 1)
        self.model_group.addButton(self.model_medium, 2)
        self.model_group.addButton(self.model_turbo, 3)
        self.model_group.addButton(self.model_large, 4)
        
        speed_layout.addWidget(self.model_small)
        speed_layout.addWidget(self.model_medium)
        speed_layout.addWidget(self.model_turbo)
        speed_layout.addWidget(self.model_large)
        self.speed_group.setLayout(speed_layout)
        left_col.addWidget(self.speed_group)
        
        # 음성 감지
        self.vad_group = QGroupBox(f"🎤 {self.tr('voice_detection')}")
        vad_layout = QVBoxLayout()
        vad_layout.setSpacing(4)
        
        self.vad_group_btn = QButtonGroup()
        self.vad_off = QRadioButton(self.tr('off'))
        self.vad_sensitive = QRadioButton(self.tr('sensitive'))
        self.vad_normal = QRadioButton(self.tr('normal'))
        self.vad_normal.setChecked(True)
        self.vad_strict = QRadioButton(self.tr('strict'))
        
        self.vad_group_btn.addButton(self.vad_off, 1)
        self.vad_group_btn.addButton(self.vad_sensitive, 2)
        self.vad_group_btn.addButton(self.vad_normal, 3)
        self.vad_group_btn.addButton(self.vad_strict, 4)
        
        vad_layout.addWidget(self.vad_off)
        vad_layout.addWidget(self.vad_sensitive)
        vad_layout.addWidget(self.vad_normal)
        vad_layout.addWidget(self.vad_strict)
        self.vad_group.setLayout(vad_layout)
        left_col.addWidget(self.vad_group)
        
        # 전처리
        self.preprocess_group = QGroupBox(f"🔧 {self.tr('preprocessing')}")
        preprocess_layout = QVBoxLayout()
        preprocess_layout.setSpacing(8)
        
        self.mdx_check = QCheckBox(self.tr('mdx_separation'))
        self.mdx_check.setChecked(True)
        self.normalize_check = QCheckBox(self.tr('normalize'))
        
        preprocess_layout.addWidget(self.mdx_check)
        preprocess_layout.addWidget(self.normalize_check)
        self.preprocess_group.setLayout(preprocess_layout)
        left_col.addWidget(self.preprocess_group)
        
        left_col.addStretch()
        options_layout.addLayout(left_col)
        
        # 오른쪽 열
        right_col = QVBoxLayout()
        right_col.setSpacing(12)
        
        # 인식 언어
        self.lang_group_box = QGroupBox(f"🌐 {self.tr('transcription_lang')}")
        lang_layout = QVBoxLayout()
        lang_layout.setSpacing(4)
        
        self.lang_group = QButtonGroup()
        self.lang_ko = QRadioButton(self.tr('korean'))
        self.lang_ko.setChecked(True)
        self.lang_en = QRadioButton(self.tr('english'))
        self.lang_ja = QRadioButton(self.tr('japanese'))
        
        self.lang_group.addButton(self.lang_ko, 1)
        self.lang_group.addButton(self.lang_en, 2)
        self.lang_group.addButton(self.lang_ja, 3)
        
        lang_layout.addWidget(self.lang_ko)
        lang_layout.addWidget(self.lang_en)
        lang_layout.addWidget(self.lang_ja)
        self.lang_group_box.setLayout(lang_layout)
        right_col.addWidget(self.lang_group_box)
        
        # 추가 기능
        self.extra_group = QGroupBox(f"✨ {self.tr('additional_features')}")
        extra_layout = QVBoxLayout()
        extra_layout.setSpacing(8)
        
        self.emotion_check = QCheckBox(self.tr('emotion'))
        self.speaker_check = QCheckBox(self.tr('speaker'))
        self.timestamp_check = QCheckBox(self.tr('timestamp'))
        self.timestamp_check.setChecked(True)
        
        extra_layout.addWidget(self.emotion_check)
        extra_layout.addWidget(self.speaker_check)
        extra_layout.addWidget(self.timestamp_check)
        self.extra_group.setLayout(extra_layout)
        right_col.addWidget(self.extra_group)
        
        # 자막 형식
        self.format_group_box = QGroupBox(f"📄 {self.tr('subtitle_format')}")
        format_layout = QHBoxLayout()
        format_layout.setSpacing(20)
        
        self.format_group = QButtonGroup()
        self.format_srt = QRadioButton("SRT")
        self.format_srt.setChecked(True)
        self.format_vtt = QRadioButton("VTT")
        
        self.format_group.addButton(self.format_srt, 1)
        self.format_group.addButton(self.format_vtt, 2)
        
        format_layout.addWidget(self.format_srt)
        format_layout.addWidget(self.format_vtt)
        format_layout.addStretch()
        self.format_group_box.setLayout(format_layout)
        right_col.addWidget(self.format_group_box)
        
        right_col.addStretch()
        options_layout.addLayout(right_col)
        
        main_layout.addLayout(options_layout)

        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 모든 버튼 높이 통일
        button_height = 50

        self.add_file_btn = QPushButton(f"📄 {self.tr('add_files')}")
        self.add_file_btn.clicked.connect(self.select_files)
        self.add_file_btn.setMinimumHeight(button_height)

        self.add_folder_btn = QPushButton(f"📁 {self.tr('add_folder')}")
        self.add_folder_btn.clicked.connect(self.select_folder)
        self.add_folder_btn.setMinimumHeight(button_height)

        self.clear_btn = QPushButton(f"🗑 {self.tr('clear_list')}")
        self.clear_btn.clicked.connect(self.clear_file_list)
        self.clear_btn.setMinimumHeight(button_height)

        self.cancel_btn = QPushButton(self.tr('cancel'))
        self.cancel_btn.clicked.connect(self.cancel_processing)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setMinimumHeight(button_height)

        self.start_btn = QPushButton(f"▶  {self.tr('start')}")
        self.start_btn.setObjectName("startButton")
        self.start_btn.clicked.connect(self.start_processing)
        self.start_btn.setMinimumWidth(280)  # 가로 더 크게
        self.start_btn.setMinimumHeight(button_height)

        self.close_btn = QPushButton(self.tr('exit'))
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setMinimumHeight(button_height)

        button_layout.addWidget(self.add_file_btn)
        button_layout.addWidget(self.add_folder_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.close_btn)

        main_layout.addLayout(button_layout)

        # 상태 표시
        self.status_label = QLabel(self.tr('ready'))
        self.status_label.setStyleSheet("""
            color: #4ade80;  /* Green 400 */
            font-weight: bold; 
            font-size: 16px;
            padding: 8px;
            background-color: #27272a;
            border-radius: 6px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # 로그 영역
        self.log_label = QLabel(f"📋 {self.tr('log')}")
        self.log_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f4f4f5;")
        main_layout.addWidget(self.log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(300)  # 150 -> 300 (2배)
        main_layout.addWidget(self.log_text)

    def on_ui_language_changed(self, index):
        """UI 언어 변경 핸들러"""
        lang_code = self.ui_lang_combo.itemData(index)
        self.change_language(lang_code)

    def handle_drop(self, event):
        """드롭 이벤트 처리"""
        paths = [u.toLocalFile() for u in event.mimeData().urls()]
        video_files = []
        video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.m4v')

        for path in paths:
            if os.path.isfile(path):
                if path.lower().endswith(video_extensions):
                    video_files.append(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(video_extensions):
                            video_files.append(os.path.join(root, file))

        if video_files:
            for vf in video_files:
                if vf not in self.video_paths:
                    self.video_paths.append(vf)
            self.update_file_list_display()
        else:
            QMessageBox.warning(self, self.tr('warning'), self.tr('no_video_files'))

    def update_file_list_display(self):
        """파일 리스트 표시 업데이트"""
        count = len(self.video_paths)
        if count == 0:
            self.drop_area.update_files([])
            return

        # QListWidget 업데이트 호출
        header_text = f"{count} {self.tr('files_selected')}"
        self.drop_area.update_files(self.video_paths, header_text)

    def select_files(self):
        """파일 선택 다이얼로그"""
        files, _ = QFileDialog.getOpenFileNames(
            self, self.tr('add_files'), '',
            'Video Files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm *.m4v);;All Files (*)'
        )
        if files:
            for f in files:
                if f not in self.video_paths:
                    self.video_paths.append(f)
            self.update_file_list_display()

    def select_folder(self):
        """폴더 선택 다이얼로그"""
        folder = QFileDialog.getExistingDirectory(self, self.tr('add_folder'), '')
        if folder:
            video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.m4v')
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(video_extensions):
                        full_path = os.path.join(root, file)
                        if full_path not in self.video_paths:
                            self.video_paths.append(full_path)
            self.update_file_list_display()

    def clear_file_list(self):
        """파일 리스트 초기화"""
        self.video_paths = []
        self.update_file_list_display()

    def get_options(self):
        """현재 설정된 옵션 반환"""
        model_map = {1: 'small', 2: 'medium', 3: 'turbo', 4: 'large-v3'}
        vad_map = {1: 'off', 2: 'sensitive', 3: 'normal', 4: 'strict'}
        lang_map = {1: 'ko', 2: 'en', 3: 'ja'}

        return {
            'model': model_map.get(self.model_group.checkedId(), 'large-v3'),
            'vad': vad_map.get(self.vad_group_btn.checkedId(), 'normal'),
            'language': lang_map.get(self.lang_group.checkedId(), 'ko'),
            'mdx_separation': self.mdx_check.isChecked(),
            'normalize_audio': self.normalize_check.isChecked(),
            'emotion_recognition': self.emotion_check.isChecked(),
            'speaker_diarization': self.speaker_check.isChecked(),
            'show_timestamp': self.timestamp_check.isChecked(),
            'subtitle_format': 'srt' if self.format_srt.isChecked() else 'vtt'
        }

    def start_processing(self):
        """처리 시작"""
        if not self.video_paths:
            QMessageBox.warning(self, self.tr('warning'), self.tr('select_video'))
            return

        options = self.get_options()
        self.log_text.clear()
        self.add_log(f"🚀 {self.tr('processing_start')} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.add_log(f"📊 {len(self.video_paths)} {self.tr('files_selected')}")

        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText(self.tr('processing'))
        self.status_label.setStyleSheet("""
            color: #f9e2af; 
            font-weight: bold; 
            font-size: 16px;
            padding: 8px;
            background-color: #252538;
            border-radius: 6px;
        """)
        # 스레드 설정
        self.thread = ProcessThread(self.video_paths, options, self.current_lang)
        self.thread.progress_signal.connect(self.add_log) # Changed from update_log to add_log to match existing method
        self.thread.item_status_signal.connect(self.drop_area.set_item_status) # 상태 시그널 연결
        self.thread.finished_signal.connect(self.processing_finished) # Changed from process_finished to processing_finished to match existing method
        self.thread.start()

    def cancel_processing(self):
        """처리 취소"""
        if hasattr(self, 'thread') and self.thread.isRunning(): # Changed from process_thread to thread
            self.thread.terminate() # Changed from process_thread to thread
            self.add_log(f"\n⚠️ {self.tr('cancelled')}")
            self.processing_finished(False, self.tr('cancelled'))

    def processing_finished(self, success, message):
        """처리 완료"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        if success:
            self.status_label.setText(self.tr('completed'))
            self.status_label.setStyleSheet("""
                color: #a6e3a1; 
                font-weight: bold; 
                font-size: 16px;
                padding: 8px;
                background-color: #252538;
                border-radius: 6px;
            """)
            QMessageBox.information(self, self.tr('complete'), message)
        else:
            self.status_label.setText(self.tr('error'))
            self.status_label.setStyleSheet("""
                color: #f38ba8; 
                font-weight: bold; 
                font-size: 16px;
                padding: 8px;
                background-color: #252538;
                border-radius: 6px;
            """)

    def add_log(self, message):
        """로그 추가"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.moveCursor(QTextCursor.End)

    def save_settings(self):
        """설정 저장"""
        settings = {
            'ui_language': self.current_lang,
            'model': self.model_group.checkedId(),
            'vad': self.vad_group_btn.checkedId(),
            'language': self.lang_group.checkedId(),
            'mdx': self.mdx_check.isChecked(),
            'normalize': self.normalize_check.isChecked(),
            'emotion': self.emotion_check.isChecked(),
            'speaker': self.speaker_check.isChecked(),
            'timestamp': self.timestamp_check.isChecked(),
            'format': self.format_group.checkedId()
        }
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)

    def load_settings(self):
        """설정 로드"""
        if not os.path.exists('settings.json'):
            return
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)

            # UI 언어 설정
            if 'ui_language' in settings:
                lang = settings['ui_language']
                idx = self.ui_lang_combo.findData(lang)
                if idx >= 0:
                    self.ui_lang_combo.setCurrentIndex(idx)
                    self.change_language(lang)

            if 'model' in settings:
                btn = self.model_group.button(settings['model'])
                if btn: btn.setChecked(True)
            if 'vad' in settings:
                btn = self.vad_group_btn.button(settings['vad'])
                if btn: btn.setChecked(True)
            if 'language' in settings:
                btn = self.lang_group.button(settings['language'])
                if btn: btn.setChecked(True)
            if 'format' in settings:
                btn = self.format_group.button(settings['format'])
                if btn: btn.setChecked(True)

            self.mdx_check.setChecked(settings.get('mdx', True))
            self.normalize_check.setChecked(settings.get('normalize', False))
            self.emotion_check.setChecked(settings.get('emotion', False))
            self.speaker_check.setChecked(settings.get('speaker', False))
            self.timestamp_check.setChecked(settings.get('timestamp', True))

        except Exception as e:
            print(f"설정 로드 오류: {e}")

    def closeEvent(self, event):
        """종료 시 설정 저장"""
        self.save_settings()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 다크 팔레트 설정
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 46))
    palette.setColor(QPalette.WindowText, QColor(205, 214, 244))
    palette.setColor(QPalette.Base, QColor(24, 24, 37))
    palette.setColor(QPalette.AlternateBase, QColor(49, 50, 68))
    palette.setColor(QPalette.ToolTipBase, QColor(205, 214, 244))
    palette.setColor(QPalette.ToolTipText, QColor(205, 214, 244))
    palette.setColor(QPalette.Text, QColor(205, 214, 244))
    palette.setColor(QPalette.Button, QColor(49, 50, 68))
    palette.setColor(QPalette.ButtonText, QColor(205, 214, 244))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(124, 77, 255))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)

    gui = SenseVoiceGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
