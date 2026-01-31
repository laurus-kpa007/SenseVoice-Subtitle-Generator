"""
CPU 병렬 처리 최적화 모듈
"""
import multiprocessing as mp
import re
from funasr import AutoModel


def process_single_segment(args):
    """
    단일 세그먼트를 독립적으로 처리 (멀티프로세싱용)
    
    Args:
        args: (audio, start, end, language, model_name) 튜플
    
    Returns:
        처리 결과 딕셔너리
    """
    audio, start, end, language, model_name = args
    
    try:
        # 각 워커 프로세스가 자체 모델 인스턴스 생성
        model = AutoModel(
            model=model_name,
            device="cpu",
            disable_update=True,
            disable_pbar=True,
            trust_remote_code=True
        )
        
        result = model.generate(
            input=audio,
            language=language,
            use_itn=True,
            data_type="sound"
        )
        
        # 결과 파싱
        if isinstance(result, list) and len(result) > 0:
            text = result[0].get('text', '') if isinstance(result[0], dict) else ''
        else:
            text = ''
        
        # 메타데이터 제거
        clean_text = re.sub(r'<\|[^|]+\|>', '', text)
        clean_text = re.sub(r'<speaker_\d+>\s*', '', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        if clean_text:
            return {
                'success': True,
                'start': start,
                'end': end,
                'text': clean_text
            }
        else:
            return {
                'success': False,
                'start': start,
                'end': end,
                'text': ''
            }
    
    except Exception as e:
        return {
            'success': False,
            'start': start,
            'end': end,
            'error': str(e)[:100]
        }


def process_segments_parallel(segments, language, model_name, num_workers=None):
    """
    여러 세그먼트를 병렬로 처리
    
    Args:
        segments: [{'audio': np.array, 'start': float, 'end': float}, ...] 리스트
        language: 대상 언어
        model_name: 사용할 모델 이름
        num_workers: 병렬 워커 수 (None이면 CPU 코어의 70%)
    
    Returns:
        성공한 세그먼트 리스트 (시간순 정렬)
    """
    if num_workers is None:
        cpu_count = mp.cpu_count()
        num_workers = max(1, int(cpu_count * 0.7))
    
    print(f"\n⚡ CPU 병렬 처리 시작")
    print(f"   CPU 코어: {mp.cpu_count()}개")
    print(f"   병렬 워커: {num_workers}개")
    print(f"   총 세그먼트: {len(segments)}개")
    print(f"   예상 속도 향상: 약 {num_workers}배")
    
    # 작업 준비
    tasks = [
        (seg['audio'], seg['start'], seg['end'], language, model_name)
        for seg in segments
    ]
    
    # 멀티프로세싱 Pool로 병렬 처리
    all_segments = []
    failed_count = 0
    
    with mp.Pool(processes=num_workers) as pool:
        # imap_unordered: 결과가 나오는대로 반환 (순서 무관, 더 빠름)
        print(f"\n처리 진행:")
        for i, result in enumerate(pool.imap_unordered(process_single_segment, tasks), 1):
            if result['success']:
                all_segments.append({
                    'start': result['start'],
                    'end': result['end'],
                    'text': result['text']
                })
                # 100개마다 진행상황 출력
                if i % 100 == 0:
                    print(f"  진행: {i}/{len(tasks)} ({i*100//len(tasks)}%)")
            else:
                failed_count += 1
                if 'error' in result:
                    print(f"  ⚠️  세그먼트 실패 [{result['start']:.1f}s-{result['end']:.1f}s]: {result.get('error', 'Unknown')}")
    
    # 시간순 정렬
    all_segments.sort(key=lambda x: x['start'])
    
    print(f"\n병렬 처리 완료!")
    print(f"  성공: {len(all_segments)}개")
    print(f"  실패: {failed_count}개")
    
    return all_segments
