import os
from datetime import timedelta


class SubtitleGenerator:
    """자막 파일 생성 클래스"""

    def __init__(self, options):
        self.options = options

    def generate(self, transcriptions, video_path):
        """
        자막 파일 생성

        Args:
            transcriptions: 음성 인식 결과 리스트
            video_path: 원본 동영상 파일 경로

        Returns:
            생성된 자막 파일 경로
        """
        subtitle_format = self.options.get('subtitle_format', 'srt')

        # 출력 파일 경로 생성
        base_path = os.path.splitext(video_path)[0]
        subtitle_path = f"{base_path}.{subtitle_format}"

        if subtitle_format == 'srt':
            self.generate_srt(transcriptions, subtitle_path)
        elif subtitle_format == 'vtt':
            self.generate_vtt(transcriptions, subtitle_path)
        else:
            raise ValueError(f"지원하지 않는 자막 형식: {subtitle_format}")

        return subtitle_path

    def generate_srt(self, transcriptions, output_path):
        """
        SRT 형식 자막 파일 생성

        Args:
            transcriptions: 음성 인식 결과 리스트
            output_path: 출력 파일 경로
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            subtitle_index = 1

            for transcription in transcriptions:
                segments = transcription.get('segments', [])

                for segment in segments:
                    start_time = segment.get('start', 0)
                    end_time = segment.get('end', 0)
                    text = segment.get('text', '').strip()

                    if not text:
                        continue

                    # 감정 정보 추가
                    if self.options.get('emotion_recognition') and segment.get('emotion'):
                        emotion = segment.get('emotion')
                        if emotion != 'neutral':
                            text = f"[{emotion}] {text}"

                    # 화자 정보 추가
                    if self.options.get('speaker_diarization') and segment.get('speaker'):
                        speaker = segment.get('speaker')
                        text = f"<{speaker}> {text}"

                    # SRT 형식으로 작성
                    f.write(f"{subtitle_index}\n")
                    f.write(f"{self.format_srt_timestamp(start_time)} --> {self.format_srt_timestamp(end_time)}\n")
                    f.write(f"{text}\n\n")

                    subtitle_index += 1

    def generate_vtt(self, transcriptions, output_path):
        """
        VTT 형식 자막 파일 생성

        Args:
            transcriptions: 음성 인식 결과 리스트
            output_path: 출력 파일 경로
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            # VTT 헤더
            f.write("WEBVTT\n\n")

            subtitle_index = 1

            for transcription in transcriptions:
                segments = transcription.get('segments', [])

                for segment in segments:
                    start_time = segment.get('start', 0)
                    end_time = segment.get('end', 0)
                    text = segment.get('text', '').strip()

                    if not text:
                        continue

                    # 감정 정보 추가
                    if self.options.get('emotion_recognition') and segment.get('emotion'):
                        emotion = segment.get('emotion')
                        if emotion != 'neutral':
                            text = f"[{emotion}] {text}"

                    # 화자 정보 추가
                    if self.options.get('speaker_diarization') and segment.get('speaker'):
                        speaker = segment.get('speaker')
                        text = f"<v {speaker}>{text}</v>"

                    # VTT 형식으로 작성
                    if self.options.get('show_timestamp'):
                        f.write(f"{subtitle_index}\n")

                    f.write(f"{self.format_vtt_timestamp(start_time)} --> {self.format_vtt_timestamp(end_time)}\n")
                    f.write(f"{text}\n\n")

                    subtitle_index += 1

    def format_srt_timestamp(self, seconds):
        """
        초를 SRT 타임스탬프 형식으로 변환 (00:00:00,000)

        Args:
            seconds: 초 단위 시간

        Returns:
            SRT 형식 타임스탬프
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def format_vtt_timestamp(self, seconds):
        """
        초를 VTT 타임스탬프 형식으로 변환 (00:00:00.000)

        Args:
            seconds: 초 단위 시간

        Returns:
            VTT 형식 타임스탬프
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def merge_short_segments(self, segments, min_duration=1.0, max_chars=80):
        """
        짧은 세그먼트를 병합하여 읽기 쉬운 자막 생성

        Args:
            segments: 자막 세그먼트 리스트
            min_duration: 최소 자막 표시 시간 (초)
            max_chars: 최대 문자 수

        Returns:
            병합된 세그먼트 리스트
        """
        if not segments:
            return []

        merged = []
        current_segment = None

        for segment in segments:
            if current_segment is None:
                current_segment = segment.copy()
                continue

            # 현재 세그먼트와 병합 가능한지 확인
            duration = current_segment['end'] - current_segment['start']
            combined_text = current_segment['text'] + ' ' + segment['text']

            if (duration < min_duration and len(combined_text) <= max_chars):
                # 병합
                current_segment['end'] = segment['end']
                current_segment['text'] = combined_text
            else:
                # 현재 세그먼트 저장하고 새로운 세그먼트 시작
                merged.append(current_segment)
                current_segment = segment.copy()

        # 마지막 세그먼트 추가
        if current_segment:
            merged.append(current_segment)

        return merged

    def split_long_text(self, text, max_chars=80):
        """
        긴 텍스트를 여러 줄로 분할

        Args:
            text: 원본 텍스트
            max_chars: 줄당 최대 문자 수

        Returns:
            분할된 텍스트
        """
        if len(text) <= max_chars:
            return text

        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # 공백 포함

            if current_length + word_length > max_chars:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)

    def add_punctuation(self, text):
        """
        자막에 적절한 구두점 추가

        Args:
            text: 원본 텍스트

        Returns:
            구두점이 추가된 텍스트
        """
        # 기본적인 구두점 추가 로직
        # 실제로는 더 정교한 NLP 모델 사용 가능

        text = text.strip()

        # 이미 구두점이 있으면 그대로 반환
        if text and text[-1] in '.!?。!?':
            return text

        # 문장 끝에 마침표 추가
        return text + '.'

    def format_subtitle_style(self, text, emotion=None):
        """
        감정에 따른 자막 스타일 지정 (VTT용)

        Args:
            text: 자막 텍스트
            emotion: 감정 정보

        Returns:
            스타일이 적용된 텍스트
        """
        emotion_styles = {
            'happy': '<c.happy>',
            'sad': '<c.sad>',
            'angry': '<c.angry>',
            'surprised': '<c.surprised>',
            'neutral': ''
        }

        if emotion and emotion in emotion_styles:
            style = emotion_styles[emotion]
            if style:
                return f"{style}{text}</c>"

        return text
