import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QRadioButton, QCheckBox,
                             QPushButton, QTextEdit, QButtonGroup, QFileDialog,
                             QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor
import json


class ProcessThread(QThread):
    """비동기 처리를 위한 스레드"""
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, video_paths, options):
        super().__init__()
        self.video_paths = video_paths
        self.options = options

    def run(self):
        """실제 처리 작업 실행"""
        try:
            from audio_processor import AudioProcessor
            from subtitle_generator import SubtitleGenerator
            import traceback

            processor = AudioProcessor(self.options)
            subtitle_gen = SubtitleGenerator(self.options)

            for video_path in self.video_paths:
                try:
                    self.progress_signal.emit(f"\n처리 시작: {os.path.basename(video_path)}")

                    # 1. 오디오 추출
                    self.progress_signal.emit("1/3 - 오디오 추출 중...")
                    audio_path = processor.extract_audio(video_path)
                    self.progress_signal.emit(f"  오디오 추출 완료: {audio_path}")

                    # 2. 음성 인식
                    self.progress_signal.emit("2/3 - 음성 인식 중...")
                    transcription = processor.transcribe(audio_path)
                    self.progress_signal.emit(f"  음성 인식 완료")

                    # 3. 자막 생성
                    self.progress_signal.emit("3/3 - 자막 파일 생성 중...")
                    subtitle_path = subtitle_gen.generate(transcription, video_path)

                    self.progress_signal.emit(f"✓ 완료: {subtitle_path}\n")

                    # 임시 오디오 파일 삭제
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                        self.progress_signal.emit(f"  임시 파일 삭제됨")

                except Exception as file_error:
                    error_detail = traceback.format_exc()
                    self.progress_signal.emit(f"\n✗ 파일 처리 실패: {os.path.basename(video_path)}")
                    self.progress_signal.emit(f"오류: {str(file_error)}")
                    self.progress_signal.emit(f"상세 정보:\n{error_detail}")
                    # 다음 파일 계속 처리
                    continue

            self.finished_signal.emit(True, "모든 파일 처리가 완료되었습니다.")

        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            error_msg = f"오류 발생: {str(e)}\n\n상세 정보:\n{error_detail}"
            self.progress_signal.emit(f"\n{error_msg}")
            self.finished_signal.emit(False, error_msg)


class SenseVoiceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_paths = []
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('SenseVoice 자막 생성기 (CUDA 최적화)')
        self.setGeometry(100, 100, 900, 700)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # 드래그 앤 드롭 영역
        self.drop_area = QLabel('동영상 파일을 드래그하거나 "로그 파일 열기" 버튼을 클릭하세요')
        self.drop_area.setAlignment(Qt.AlignCenter)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 60px;
                background-color: #f9f9f9;
                font-size: 24px;
                color: #666;
            }
        """)
        self.drop_area.setAcceptDrops(True)
        self.drop_area.dragEnterEvent = self.drag_enter_event
        self.drop_area.dropEvent = self.drop_event
        main_layout.addWidget(self.drop_area)

        # 옵션 영역
        options_layout = QVBoxLayout()

        # 처리 속도
        model_layout = QHBoxLayout()
        label_font = QFont()
        label_font.setPointSize(11)
        speed_label = QLabel('처리 속도:')
        speed_label.setFont(label_font)
        model_layout.addWidget(speed_label)

        self.model_group = QButtonGroup()

        radio_font = QFont()
        radio_font.setPointSize(10)

        self.model_small = QRadioButton('빠름 (Small)')
        self.model_small.setFont(radio_font)
        self.model_medium = QRadioButton('균형 (Medium)')
        self.model_medium.setFont(radio_font)
        self.model_turbo = QRadioButton('고품질 (Turbo)')
        self.model_turbo.setFont(radio_font)
        self.model_large = QRadioButton('최고품질 (Large-v3) ★ 권장')
        self.model_large.setFont(radio_font)

        self.model_large.setChecked(True)  # 최고품질을 기본값으로 설정

        self.model_group.addButton(self.model_small, 1)
        self.model_group.addButton(self.model_medium, 2)
        self.model_group.addButton(self.model_turbo, 3)
        self.model_group.addButton(self.model_large, 4)

        model_layout.addWidget(self.model_small)
        model_layout.addWidget(self.model_medium)
        model_layout.addWidget(self.model_turbo)
        model_layout.addWidget(self.model_large)
        model_layout.addStretch()

        options_layout.addLayout(model_layout)

        # 음성 감지(VAD)
        vad_layout = QHBoxLayout()
        vad_label = QLabel('음성 감지(VAD):')
        vad_label.setFont(label_font)
        vad_layout.addWidget(vad_label)

        self.vad_group = QButtonGroup()
        self.vad_off = QRadioButton('끄기 (전체)')
        self.vad_off.setFont(radio_font)
        self.vad_sensitive = QRadioButton('만감 (많이 감지)')
        self.vad_sensitive.setFont(radio_font)
        self.vad_normal = QRadioButton('보통')
        self.vad_normal.setFont(radio_font)
        self.vad_strict = QRadioButton('엄격 (적게 감지)')
        self.vad_strict.setFont(radio_font)

        self.vad_normal.setChecked(True)

        self.vad_group.addButton(self.vad_off, 1)
        self.vad_group.addButton(self.vad_sensitive, 2)
        self.vad_group.addButton(self.vad_normal, 3)
        self.vad_group.addButton(self.vad_strict, 4)

        vad_layout.addWidget(self.vad_off)
        vad_layout.addWidget(self.vad_sensitive)
        vad_layout.addWidget(self.vad_normal)
        vad_layout.addWidget(self.vad_strict)
        vad_layout.addStretch()

        options_layout.addLayout(vad_layout)

        # 전처리 옵션
        preprocess_layout = QHBoxLayout()
        pre_label = QLabel('전처리:')
        pre_label.setFont(label_font)
        preprocess_layout.addWidget(pre_label)
        self.mdx_check = QCheckBox('MDX Kim 음성 분리 사용 (드리지만 품질 향상)')
        self.mdx_check.setFont(radio_font)
        self.mdx_check.setChecked(True)
        preprocess_layout.addWidget(self.mdx_check)
        preprocess_layout.addStretch()

        options_layout.addLayout(preprocess_layout)

        # 음향 정규화
        normalize_layout = QHBoxLayout()
        self.normalize_check = QCheckBox('음향 정규화 (EBU R128 라우드니스 정규화 - 작은 소리 증폭)')
        self.normalize_check.setFont(radio_font)
        normalize_layout.addWidget(self.normalize_check)
        normalize_layout.addStretch()

        options_layout.addLayout(normalize_layout)

        # 언어 선택
        lang_layout = QHBoxLayout()
        lang_label = QLabel('언어 선택:')
        lang_label.setFont(label_font)
        lang_layout.addWidget(lang_label)

        self.lang_group = QButtonGroup()
        self.lang_ko = QRadioButton('한국어')
        self.lang_ko.setFont(radio_font)
        self.lang_en = QRadioButton('영어')
        self.lang_en.setFont(radio_font)
        self.lang_ja = QRadioButton('일본어')
        self.lang_ja.setFont(radio_font)

        self.lang_ko.setChecked(True)  # 한국어를 기본값으로 설정

        self.lang_group.addButton(self.lang_ko, 1)
        self.lang_group.addButton(self.lang_en, 2)
        self.lang_group.addButton(self.lang_ja, 3)

        lang_layout.addWidget(self.lang_ko)
        lang_layout.addWidget(self.lang_en)
        lang_layout.addWidget(self.lang_ja)
        lang_layout.addStretch()

        options_layout.addLayout(lang_layout)

        # 추가 기능
        extra_layout = QHBoxLayout()
        self.emotion_check = QCheckBox('감정 인식')
        self.emotion_check.setFont(radio_font)
        self.speaker_check = QCheckBox('화자 분리')
        self.speaker_check.setFont(radio_font)
        self.timestamp_check = QCheckBox('타임스탬프 표시')
        self.timestamp_check.setFont(radio_font)
        self.timestamp_check.setChecked(True)

        extra_layout.addWidget(self.emotion_check)
        extra_layout.addWidget(self.speaker_check)
        extra_layout.addWidget(self.timestamp_check)
        extra_layout.addStretch()

        options_layout.addLayout(extra_layout)

        # 자막 형식
        format_layout = QHBoxLayout()
        format_label = QLabel('자막 형식:')
        format_label.setFont(label_font)
        format_layout.addWidget(format_label)
        self.format_group = QButtonGroup()
        self.format_srt = QRadioButton('SRT')
        self.format_srt.setFont(radio_font)
        self.format_vtt = QRadioButton('VTT')
        self.format_vtt.setFont(radio_font)

        self.format_srt.setChecked(True)

        self.format_group.addButton(self.format_srt, 1)
        self.format_group.addButton(self.format_vtt, 2)

        format_layout.addWidget(self.format_srt)
        format_layout.addWidget(self.format_vtt)
        format_layout.addStretch()

        options_layout.addLayout(format_layout)

        main_layout.addLayout(options_layout)

        # 버튼 영역
        button_layout = QHBoxLayout()

        button_font = QFont()
        button_font.setPointSize(10)

        self.add_file_btn = QPushButton('📄 파일 추가')
        self.add_file_btn.setFont(button_font)
        self.add_file_btn.clicked.connect(self.select_files)

        self.add_folder_btn = QPushButton('📁 폴더 추가')
        self.add_folder_btn.setFont(button_font)
        self.add_folder_btn.clicked.connect(self.select_folder)

        self.clear_btn = QPushButton('🗑 목록 초기화')
        self.clear_btn.setFont(button_font)
        self.clear_btn.clicked.connect(self.clear_file_list)

        self.cancel_btn = QPushButton('취소')
        self.cancel_btn.setFont(button_font)
        self.cancel_btn.clicked.connect(self.cancel_processing)
        self.cancel_btn.setEnabled(False)

        self.start_btn = QPushButton('▶ 실행')
        self.start_btn.setFont(button_font)
        self.start_btn.clicked.connect(self.start_processing)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 24pt;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        self.close_btn = QPushButton('종료')
        self.close_btn.setFont(button_font)
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.add_file_btn)
        button_layout.addWidget(self.add_folder_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.close_btn)

        main_layout.addLayout(button_layout)

        # 준비됨 표시
        self.status_label = QLabel('준비됨')
        self.status_label.setStyleSheet('color: green; font-weight: bold; font-size: 14px;')
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # 실행 로그 영역
        log_label = QLabel('실행 로그:')
        log_label.setFont(label_font)
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 24px;
            }
        """)
        main_layout.addWidget(self.log_text)

        # 초기 로그 표시
        self.add_log(f"로그 파일 위치: {self.get_log_path()}")
        self.add_log("문제 발생 시 '로그 파일 열기' 버튼을 클릭하여 상세 로그를 확인하세요.")

    def drag_enter_event(self, event):
        """드래그 엔터 이벤트"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """드롭 이벤트 - 파일 및 폴더 지원"""
        paths = [u.toLocalFile() for u in event.mimeData().urls()]
        video_files = []

        # 지원하는 동영상 확장자
        video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.m4v')

        for path in paths:
            if os.path.isfile(path):
                # 파일인 경우
                if path.lower().endswith(video_extensions):
                    video_files.append(path)
            elif os.path.isdir(path):
                # 폴더인 경우 - 재귀적으로 모든 동영상 파일 찾기
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(video_extensions):
                            video_files.append(os.path.join(root, file))

        if video_files:
            # 기존 리스트에 추가 (중복 제거)
            for vf in video_files:
                if vf not in self.video_paths:
                    self.video_paths.append(vf)

            self.update_file_list_display()
        else:
            QMessageBox.warning(self, '경고', '지원하는 동영상 파일이 없습니다.')

    def update_file_list_display(self):
        """파일 리스트 표시 업데이트"""
        if not self.video_paths:
            self.drop_area.setText('동영상 파일/폴더를 드래그하거나 버튼을 클릭하세요')
            return

        display_text = f'📁 {len(self.video_paths)}개 파일 선택됨\n\n'

        # 처음 10개 파일만 표시
        for i, f in enumerate(self.video_paths[:10]):
            display_text += f'{i+1}. {os.path.basename(f)}\n'

        if len(self.video_paths) > 10:
            display_text += f'\n... 외 {len(self.video_paths) - 10}개'

        self.drop_area.setText(display_text)

    def select_files(self):
        """파일 선택 다이얼로그"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            '동영상 파일 선택',
            '',
            'Video Files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv *.webm *.m4v);;All Files (*)'
        )

        if files:
            # 기존 리스트에 추가 (중복 제거)
            for f in files:
                if f not in self.video_paths:
                    self.video_paths.append(f)
            self.update_file_list_display()

    def select_folder(self):
        """폴더 선택 다이얼로그"""
        folder = QFileDialog.getExistingDirectory(
            self,
            '동영상 폴더 선택',
            ''
        )

        if folder:
            # 지원하는 동영상 확장자
            video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.m4v')
            video_files = []

            # 폴더 내 모든 동영상 파일 찾기
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(video_extensions):
                        video_files.append(os.path.join(root, file))

            if video_files:
                # 기존 리스트에 추가 (중복 제거)
                for vf in video_files:
                    if vf not in self.video_paths:
                        self.video_paths.append(vf)
                self.update_file_list_display()
                QMessageBox.information(self, '완료', f'{len(video_files)}개의 동영상 파일을 찾았습니다.')
            else:
                QMessageBox.warning(self, '경고', '폴더에 동영상 파일이 없습니다.')

    def clear_file_list(self):
        """파일 리스트 초기화"""
        self.video_paths = []
        self.update_file_list_display()

    def get_options(self):
        """현재 설정된 옵션 반환"""
        model_map = {1: 'small', 2: 'medium', 3: 'turbo', 4: 'large-v3'}
        vad_map = {1: 'off', 2: 'sensitive', 3: 'normal', 4: 'strict'}
        lang_map = {1: 'ko', 2: 'en', 3: 'ja'}  # 한국어를 1번으로 변경

        return {
            'model': model_map.get(self.model_group.checkedId(), 'large-v3'),  # 기본값: 최고품질
            'vad': vad_map.get(self.vad_group.checkedId(), 'normal'),
            'language': lang_map.get(self.lang_group.checkedId(), 'ko'),  # 기본값: 한국어
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
            QMessageBox.warning(self, '경고', '처리할 동영상 파일을 선택해주세요.')
            return

        options = self.get_options()

        # 로그 초기화
        self.log_text.clear()
        self.add_log(f"처리 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.add_log(f"선택된 파일 수: {len(self.video_paths)}")
        self.add_log(f"옵션: {options}\n")

        # UI 상태 변경
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText('처리 중...')
        self.status_label.setStyleSheet('color: orange; font-weight: bold;')

        # 처리 스레드 시작
        self.process_thread = ProcessThread(self.video_paths, options)
        self.process_thread.progress_signal.connect(self.add_log)
        self.process_thread.finished_signal.connect(self.processing_finished)
        self.process_thread.start()

    def cancel_processing(self):
        """처리 취소"""
        if hasattr(self, 'process_thread') and self.process_thread.isRunning():
            self.process_thread.terminate()
            self.add_log("\n처리가 취소되었습니다.")
            self.processing_finished(False, "사용자가 취소했습니다.")

    def processing_finished(self, success, message):
        """처리 완료"""
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        if success:
            self.status_label.setText('완료')
            self.status_label.setStyleSheet('color: green; font-weight: bold;')
            QMessageBox.information(self, '완료', message)
        else:
            self.status_label.setText('오류 발생')
            self.status_label.setStyleSheet('color: red; font-weight: bold;')
            QMessageBox.critical(self, '오류', message)

        self.add_log(f"\n완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def add_log(self, message):
        """로그 추가"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.append(f"{timestamp} - {message}")
        self.log_text.moveCursor(QTextCursor.End)

        # 파일에도 로그 저장
        log_path = self.get_log_path()
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - {message}\n")

    def get_log_path(self):
        """로그 파일 경로 반환"""
        log_dir = os.path.join(os.getcwd(), 'logs')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(log_dir, f'sensevoice_gui_{timestamp}.log')

    def save_settings(self):
        """설정 저장"""
        settings = {
            'model': self.model_group.checkedId(),
            'vad': self.vad_group.checkedId(),
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

            # 설정 적용
            if 'model' in settings:
                btn = self.model_group.button(settings['model'])
                if btn:
                    btn.setChecked(True)

            if 'vad' in settings:
                btn = self.vad_group.button(settings['vad'])
                if btn:
                    btn.setChecked(True)

            if 'language' in settings:
                btn = self.lang_group.button(settings['language'])
                if btn:
                    btn.setChecked(True)

            self.mdx_check.setChecked(settings.get('mdx', True))
            self.normalize_check.setChecked(settings.get('normalize', False))
            self.emotion_check.setChecked(settings.get('emotion', False))
            self.speaker_check.setChecked(settings.get('speaker', False))
            self.timestamp_check.setChecked(settings.get('timestamp', True))

            if 'format' in settings:
                btn = self.format_group.button(settings['format'])
                if btn:
                    btn.setChecked(True)

        except Exception as e:
            print(f"설정 로드 오류: {e}")

    def closeEvent(self, event):
        """종료 시 설정 저장"""
        self.save_settings()
        event.accept()


def main():
    app = QApplication(sys.argv)

    # 폰트 설정
    font = QFont()
    font.setFamily('맑은 고딕')
    font.setPointSize(9)
    app.setFont(font)

    gui = SenseVoiceGUI()
    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
