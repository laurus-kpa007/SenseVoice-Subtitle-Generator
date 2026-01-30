import os
import ffmpeg
import tempfile
from datetime import datetime


class AudioProcessor:
    """오디오 추출 및 전처리 클래스"""

    def __init__(self, options):
        self.options = options

    def extract_audio(self, video_path):
        """
        MP4 동영상에서 오디오를 추출

        Args:
            video_path: 동영상 파일 경로

        Returns:
            추출된 오디오 파일 경로
        """
        # 임시 오디오 파일 경로 생성
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = os.path.join(temp_dir, f'temp_audio_{timestamp}.wav')

        try:
            # FFmpeg를 사용하여 오디오 추출
            stream = ffmpeg.input(video_path)

            # 오디오 설정
            stream = ffmpeg.output(
                stream,
                audio_path,
                acodec='pcm_s16le',  # WAV 포맷
                ac=1,                 # 모노 채널
                ar='16000',           # 16kHz 샘플레이트 (SenseVoice 권장)
                loglevel='error'
            )

            # 기존 파일이 있으면 덮어쓰기
            ffmpeg.run(stream, overwrite_output=True)

            # 전처리 적용
            if self.options.get('mdx_separation', False):
                audio_path = self.apply_mdx_separation(audio_path)

            if self.options.get('normalize_audio', False):
                audio_path = self.normalize_audio(audio_path)

            return audio_path

        except ffmpeg.Error as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise Exception(f"오디오 추출 실패: {error_msg}")

    def apply_mdx_separation(self, audio_path):
        """
        MDX Kim 음성 분리 적용 (배경음악/소음 제거)

        Args:
            audio_path: 원본 오디오 파일 경로

        Returns:
            처리된 오디오 파일 경로
        """
        try:
            # 실제 환경에서는 demucs 또는 spleeter 같은 라이브러리 사용
            # 여기서는 간단한 노이즈 리덕션 필터 적용
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(temp_dir, f'separated_{timestamp}.wav')

            stream = ffmpeg.input(audio_path)

            # 노이즈 리덕션 및 음성 강화 필터
            stream = ffmpeg.filter(stream, 'highpass', f=200)  # 저주파 노이즈 제거
            stream = ffmpeg.filter(stream, 'lowpass', f=3000)  # 고주파 노이즈 제거

            stream = ffmpeg.output(
                stream,
                output_path,
                acodec='pcm_s16le',
                ac=1,
                ar='16000',
                loglevel='error'
            )

            ffmpeg.run(stream, overwrite_output=True)

            # 원본 파일 삭제
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return output_path

        except Exception as e:
            print(f"음성 분리 경고: {e}, 원본 파일 사용")
            return audio_path

    def normalize_audio(self, audio_path):
        """
        EBU R128 라우드니스 정규화 적용

        Args:
            audio_path: 원본 오디오 파일 경로

        Returns:
            정규화된 오디오 파일 경로
        """
        try:
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(temp_dir, f'normalized_{timestamp}.wav')

            stream = ffmpeg.input(audio_path)

            # 라우드니스 정규화 필터 적용
            stream = ffmpeg.filter(stream, 'loudnorm', I=-16, TP=-1.5, LRA=11)

            stream = ffmpeg.output(
                stream,
                output_path,
                acodec='pcm_s16le',
                ac=1,
                ar='16000',
                loglevel='error'
            )

            ffmpeg.run(stream, overwrite_output=True)

            # 원본 파일 삭제
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return output_path

        except Exception as e:
            print(f"정규화 경고: {e}, 원본 파일 사용")
            return audio_path

    def transcribe(self, audio_path):
        """
        SenseVoice를 사용하여 오디오를 텍스트로 변환
        VAD를 먼저 실행하여 세그먼트를 나눈 후 각각 인식

        Args:
            audio_path: 오디오 파일 경로

        Returns:
            인식 결과 (타임스탬프 포함)
        """
        try:
            from funasr import AutoModel
            import librosa
            import numpy as np

            # 디바이스 설정 - GPU 호환성 확인
            import torch

            # CUDA 가용성 확인
            cuda_available = torch.cuda.is_available()

            if cuda_available:
                try:
                    # GPU 호환성 테스트
                    gpu_name = torch.cuda.get_device_name(0)
                    cuda_version = torch.version.cuda

                    # 간단한 텐서 연산으로 GPU 작동 확인
                    test_tensor = torch.zeros(1).cuda()
                    _ = test_tensor + 1

                    device = "cuda:0"
                    print(f"🚀 GPU 사용: {gpu_name}")
                    print(f"   CUDA 버전: {cuda_version}")
                    print(f"   GPU 메모리: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")

                except Exception as gpu_error:
                    print(f"\n⚠️  GPU 호환성 오류 발생!")
                    print(f"⚠️  오류: {str(gpu_error)[:100]}")
                    print(f"\n💡 해결 방법:")
                    print(f"   RTX 5070 Ti는 최신 GPU로 PyTorch CUDA 12.4+ 필요")
                    print(f"   1. install_gpu.bat 실행")
                    print(f"   2. 또는 수동 설치:")
                    print(f"      pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124")
                    print(f"\n⚠️  임시로 CPU 모드로 전환합니다...\n")
                    device = "cpu"
            else:
                device = "cpu"
                print(f"⚠️  CUDA를 사용할 수 없습니다. CPU 모드로 실행")

            print(f"사용 디바이스: {device}")

            # 1단계: VAD 모델로 음성 구간 탐지
            print("\n[1단계] VAD (음성 구간 탐지) 실행 중...")

            try:
                vad_kwargs = self.get_vad_kwargs()

                vad_model = AutoModel(
                    model="fsmn-vad",
                    device=device,
                    disable_update=True,
                    trust_remote_code=True  # 공식 모델이므로 안전
                )
                print(f"   VAD 모델 로드 완료")

            except Exception as vad_load_error:
                raise Exception(f"VAD 모델 로드 실패: {str(vad_load_error)}")

            try:
                vad_result = vad_model.generate(input=audio_path)
                print(f"   VAD 완료! 결과 타입: {type(vad_result)}")

            except RuntimeError as cuda_error:
                if "CUDA" in str(cuda_error):
                    raise Exception(f"GPU 호환성 오류 - CPU 모드로 재시도하거나 install_gpu.bat를 실행하세요: {str(cuda_error)}")
                else:
                    raise Exception(f"VAD 실행 실패: {str(cuda_error)}")

            except Exception as vad_error:
                raise Exception(f"VAD 음성 구간 탐지 실패: {str(vad_error)}")

            # VAD 세그먼트 추출
            vad_segments = []
            try:
                if isinstance(vad_result, list) and len(vad_result) > 0:
                    vad_data = vad_result[0]
                    if isinstance(vad_data, dict) and 'value' in vad_data:
                        # value는 [[start_ms, end_ms], ...] 형태
                        segments_list = vad_data['value']
                        print(f"   VAD 세그먼트 수: {len(segments_list)}")

                        for seg in segments_list:
                            if isinstance(seg, (list, tuple)) and len(seg) >= 2:
                                start_ms, end_ms = seg[0], seg[1]
                                vad_segments.append({
                                    'start': start_ms / 1000.0,  # 밀리초 -> 초
                                    'end': end_ms / 1000.0
                                })

                        print(f"   VAD로 {len(vad_segments)}개 음성 구간 탐지됨")
                        for idx, seg in enumerate(vad_segments[:5]):  # 처음 5개만 출력
                            print(f"     세그먼트 {idx}: {seg['start']:.2f}s ~ {seg['end']:.2f}s")
                        if len(vad_segments) > 5:
                            print(f"     ... 외 {len(vad_segments)-5}개")

            except Exception as parse_error:
                print(f"   ⚠️  VAD 결과 파싱 경고: {str(parse_error)}")
                vad_segments = []

            # VAD 세그먼트가 없으면 전체를 하나로
            if not vad_segments:
                print("   VAD 세그먼트 없음 - 전체 오디오를 하나로 처리")
                import wave
                try:
                    with wave.open(audio_path, 'rb') as wf:
                        duration = wf.getnframes() / wf.getframerate()
                        vad_segments = [{'start': 0, 'end': duration}]
                        print(f"   전체 길이: {duration:.2f}초")
                except Exception as wave_error:
                    print(f"   ⚠️  오디오 파일 정보 읽기 실패, 기본값 사용: {str(wave_error)}")
                    vad_segments = [{'start': 0, 'end': 90}]  # 기본값

            # 2단계: SenseVoice 모델로 각 세그먼트 인식
            print("\n[2단계] 음성 인식 모델 로드 중...")

            try:
                # 언어 설정
                language = self.options.get('language', 'auto')
                print(f"   GUI에서 전달받은 언어 설정: '{language}'")

                lang_map = {'ja': 'ja', 'en': 'en', 'ko': 'ko', 'zh': 'zh', 'auto': 'auto'}
                target_lang = lang_map.get(language, 'auto')
                print(f"   변환된 언어 코드: '{target_lang}'")

                # 일본어 선택 시 알림
                if target_lang == 'ja':
                    model_name = self.get_model_name()
                    print(f"   ℹ️  일본어 모드 (SenseVoice는 다국어 자동 감지)")
                else:
                    model_name = self.get_model_name()

                # ASR 모델 로드
                asr_model = AutoModel(
                    model=model_name,
                    device=device,
                    disable_update=True,
                    disable_pbar=False,
                    trust_remote_code=True
                )
                print(f"   ASR 모델 로드 완료: {model_name}")
                print(f"   설정된 대상 언어: {target_lang}")

            except Exception as model_load_error:
                raise Exception(f"ASR 모델 로드 실패: {str(model_load_error)}")

            # 오디오 로드
            try:
                audio_data, sr = librosa.load(audio_path, sr=16000, mono=True)
                total_duration = len(audio_data) / sr
                print(f"   오디오 로드 완료: {total_duration:.2f}초, 샘플레이트: {sr}Hz")

            except Exception as audio_load_error:
                raise Exception(f"오디오 파일 로드 실패: {str(audio_load_error)}")

            # 각 VAD 세그먼트 인식 (GPU 배치 처리 최적화)
            all_segments = []

            # GPU 사용 시 배치 크기 설정
            batch_size = 8 if device.startswith("cuda") else 1
            print(f"\n배치 크기: {batch_size} (GPU 가속 {'활성화' if device.startswith('cuda') else '비활성화'})")

            # 세그먼트 준비
            valid_segments = []
            for vad_seg in vad_segments:
                start_sec = vad_seg['start']
                end_sec = vad_seg['end']

                start_sample = int(start_sec * sr)
                end_sample = int(end_sec * sr)
                segment_audio = audio_data[start_sample:end_sample]

                # 너무 짧은 세그먼트는 스킵
                if len(segment_audio) >= sr * 0.3:  # 0.3초 이상
                    valid_segments.append({
                        'audio': segment_audio,
                        'start': start_sec,
                        'end': end_sec
                    })

            print(f"처리할 세그먼트 수: {len(valid_segments)}개")

            # 배치 단위로 처리
            import re
            failed_segments = []

            for batch_idx in range(0, len(valid_segments), batch_size):
                batch = valid_segments[batch_idx:batch_idx + batch_size]
                batch_audios = [seg['audio'] for seg in batch]

                batch_num = batch_idx//batch_size + 1
                total_batches = (len(valid_segments) + batch_size - 1)//batch_size
                print(f"\n배치 {batch_num}/{total_batches}: {len(batch)}개 세그먼트 처리 중...")

                try:
                    # 배치 음성 인식
                    if len(batch_audios) == 1:
                        # 단일 세그먼트
                        result = asr_model.generate(
                            input=batch_audios[0],
                            language=target_lang,
                            use_itn=True,
                            data_type="sound"
                        )
                        results = [result]
                    else:
                        # 다중 세그먼트 배치 처리
                        try:
                            result = asr_model.generate(
                                input=batch_audios,
                                language=target_lang,
                                use_itn=True,
                                data_type="sound"
                            )
                            results = result if isinstance(result, list) else [result]
                        except Exception as batch_error:
                            # 배치 처리 실패 시 개별 처리
                            print(f"  ⚠️  배치 처리 실패: {str(batch_error)[:50]}")
                            print(f"  개별 처리로 전환...")
                            results = []
                            for i, audio in enumerate(batch_audios):
                                try:
                                    r = asr_model.generate(
                                        input=audio,
                                        language=target_lang,
                                        use_itn=True,
                                        data_type="sound"
                                    )
                                    results.append(r)
                                except Exception as single_error:
                                    print(f"  ⚠️  세그먼트 {i+1} 처리 실패: {str(single_error)[:30]}")
                                    results.append(None)

                    # 결과 파싱
                    for seg, result in zip(batch, results):
                        try:
                            if result is None:
                                failed_segments.append(seg)
                                continue

                            if isinstance(result, list) and len(result) > 0:
                                text = result[0].get('text', '') if isinstance(result[0], dict) else ''
                            else:
                                text = ''

                            # 메타데이터 제거
                            clean_text = re.sub(r'<\|[^|]+\|>', '', text)
                            clean_text = re.sub(r'<speaker_\d+>\s*', '', clean_text)
                            clean_text = re.sub(r'\s+', ' ', clean_text).strip()

                            if clean_text:
                                all_segments.append({
                                    'start': seg['start'],
                                    'end': seg['end'],
                                    'text': clean_text
                                })
                                print(f"  ✓ [{seg['start']:.1f}s-{seg['end']:.1f}s] {clean_text[:80]}...")
                            else:
                                print(f"  ⚠️  [{seg['start']:.1f}s-{seg['end']:.1f}s] 텍스트 없음")

                        except Exception as parse_error:
                            print(f"  ⚠️  결과 파싱 실패: {str(parse_error)}")
                            failed_segments.append(seg)

                except Exception as batch_critical_error:
                    print(f"  ❌ 배치 처리 중 심각한 오류: {str(batch_critical_error)}")
                    failed_segments.extend(batch)

            # 처리 결과 요약
            print(f"\n" + "="*60)
            print(f"처리 완료!")
            print(f"  - 성공: {len(all_segments)}개 세그먼트")
            print(f"  - 실패: {len(failed_segments)}개 세그먼트")
            if failed_segments:
                print(f"  ⚠️  실패한 세그먼트:")
                for seg in failed_segments[:3]:
                    print(f"     [{seg['start']:.1f}s-{seg['end']:.1f}s]")
                if len(failed_segments) > 3:
                    print(f"     ... 외 {len(failed_segments)-3}개")
            print("="*60)

            # 결과 반환
            if all_segments:
                transcription = {
                    'text': ' '.join([seg['text'] for seg in all_segments]),
                    'segments': all_segments,
                    'language': target_lang
                }
                return [transcription]
            else:
                if failed_segments:
                    raise Exception(f"모든 세그먼트 처리 실패 ({len(failed_segments)}개)")
                else:
                    raise Exception("처리할 음성 구간을 찾을 수 없습니다")

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"❌ 음성 인식 중 오류 발생")
            print(f"{'='*60}")
            print(f"오류 유형: {type(e).__name__}")
            print(f"오류 메시지: {str(e)}")
            print(f"\n상세 스택:")
            print(error_trace)
            print(f"{'='*60}")
            raise Exception(f"음성 인식 실패: {str(e)}")

    def get_model_name(self):
        """모델 크기에 따른 모델 이름 반환"""
        # SenseVoice Small: 최고의 다국어 모델 (50+ 언어, 400k 시간 학습)
        # Paraformer Large: 더 큰 모델이지만 중국어 특화
        model_map = {
            'small': 'iic/SenseVoiceSmall',
            'medium': 'iic/SenseVoiceSmall',
            'turbo': 'iic/SenseVoiceSmall',
            'large-v3': 'iic/SenseVoiceSmall',  # SenseVoice는 Small 버전만 존재
            # 'large-v3': 'damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',  # 더 큰 모델 (중국어 특화)
        }

        model_size = self.options.get('model', 'large-v3')  # 기본값: 최고품질
        return model_map.get(model_size, 'iic/SenseVoiceSmall')

    def get_vad_kwargs(self):
        """VAD 설정 반환"""
        vad_mode = self.options.get('vad', 'normal')

        vad_settings = {
            'off': None,
            'sensitive': {
                'max_single_segment_time': 30000,
                'speech_noise_thres': 0.3,  # 낮은 임계값
            },
            'normal': {
                'max_single_segment_time': 30000,
                'speech_noise_thres': 0.5,  # 중간 임계값
            },
            'strict': {
                'max_single_segment_time': 30000,
                'speech_noise_thres': 0.7,  # 높은 임계값
            }
        }

        return vad_settings.get(vad_mode, vad_settings['normal'])

    def parse_result(self, result, segment_index=0):
        """
        SenseVoice 결과 파싱

        Args:
            result: SenseVoice 인식 결과
            segment_index: VAD 세그먼트 인덱스 (여러 세그먼트로 분리된 경우)

        Returns:
            파싱된 결과 딕셔너리
        """
        import re

        print(f"\n=== parse_result 호출 (세그먼트 #{segment_index}) ===")
        print(f"입력 타입: {type(result)}")

        def clean_sensevoice_text(text):
            """SenseVoice 메타데이터 태그 제거"""
            # <|언어|>, <|감정|>, <|타입|> 등 메타데이터 제거
            text = re.sub(r'<\|[^|]+\|>', '', text)
            # <speaker_N> 제거
            text = re.sub(r'<speaker_\d+>\s*', '', text)
            # 연속된 공백 제거
            text = re.sub(r'\s+', ' ', text)
            # 앞뒤 공백 제거
            text = text.strip()
            return text

        # SenseVoice 결과 구조에 맞게 파싱
        if isinstance(result, dict):
            raw_text = result.get('text', '')
            print(f"원본 텍스트: {raw_text[:200]}...")

            # 메타데이터 제거
            clean_text = clean_sensevoice_text(raw_text)
            print(f"정제된 텍스트: {clean_text[:200]}...")

            segments = []

            # sentence_info에서 세그먼트 추출 (FunASR의 표준 출력)
            sentence_info = result.get('sentence_info', [])
            print(f"sentence_info 존재: {len(sentence_info) if sentence_info else 0}개 세그먼트")

            if sentence_info and isinstance(sentence_info, list):
                # sentence_info가 있는 경우 - 각 문장별로 세그먼트 생성
                for sent in sentence_info:
                    if isinstance(sent, dict):
                        sent_text = clean_sensevoice_text(sent.get('text', ''))
                        if sent_text:  # 텍스트가 있는 경우만
                            segments.append({
                                'start': sent.get('start', 0),
                                'end': sent.get('end', 0),
                                'text': sent_text
                            })
            else:
                # sentence_info가 없는 경우 - timestamp 필드 확인
                timestamp = result.get('timestamp', None)
                print(f"timestamp 필드: {type(timestamp)}")

                if timestamp and isinstance(timestamp, list) and len(timestamp) > 0:
                    # timestamp가 있는 경우
                    print(f"timestamp 길이: {len(timestamp)}")

                    # timestamp 구조 확인
                    if len(timestamp) > 0:
                        print(f"timestamp[0] 샘플: {timestamp[0]}")

                    # timestamp는 보통 [[start, end], [start, end], ...] 형태
                    for idx, ts_info in enumerate(timestamp):
                        if isinstance(ts_info, (list, tuple)) and len(ts_info) >= 2:
                            start_ms = ts_info[0]
                            end_ms = ts_info[1]

                            # 밀리초를 초로 변환
                            start_sec = start_ms / 1000.0 if start_ms > 1000 else start_ms
                            end_sec = end_ms / 1000.0 if end_ms > 1000 else end_ms

                            # 전체 텍스트를 세그먼트 개수로 나눔
                            words = clean_text.split()
                            segment_size = max(1, len(words) // len(timestamp))
                            start_word = idx * segment_size
                            end_word = start_word + segment_size if idx < len(timestamp) - 1 else len(words)
                            segment_text = ' '.join(words[start_word:end_word])

                            if segment_text:
                                segments.append({
                                    'start': start_sec,
                                    'end': end_sec,
                                    'text': segment_text
                                })

                if not segments:
                    # 타임스탬프도 없으면 전체 텍스트를 하나의 세그먼트로
                    print("세그먼트 정보 없음 - 전체를 단일 세그먼트로 처리")
                    if clean_text:
                        segments.append({
                            'start': 0,
                            'end': len(clean_text.split()) * 0.5,
                            'text': clean_text
                        })

            parsed = {
                'text': clean_text,
                'segments': segments,
                'language': result.get('language', 'unknown')
            }
            print(f"최종 세그먼트 수: {len(segments)}")
            if segments:
                print(f"첫 세그먼트: {segments[0]}")
            return parsed

        # 문자열인 경우
        elif isinstance(result, str):
            clean_text = clean_sensevoice_text(result)
            parsed = {
                'text': clean_text,
                'segments': [{'start': 0, 'end': len(clean_text.split()) * 0.5, 'text': clean_text}],
                'language': 'unknown'
            }
            print(f"문자열 파싱 결과: {parsed}")
            return parsed

        # 기타
        else:
            text = clean_sensevoice_text(str(result))
            parsed = {
                'text': text,
                'segments': [{'start': 0, 'end': 0, 'text': text}],
                'language': 'unknown'
            }
            print(f"기본 파싱 결과: {parsed}")
            return parsed
