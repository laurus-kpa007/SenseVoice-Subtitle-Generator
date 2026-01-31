"""
멀티스레딩 기반 병렬 처리 모듈 (모델 공유)
"""
import threading
import queue
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_segment_batch(model, segments_batch, language):
    """
    단일 스레드에서 여러 세그먼트를 배치 처리
    
    Args:
        model: 사전 로드된 ASR 모델 (스레드 간 공유)
        segments_batch: 처리할 세그먼트 리스트
        language: 대상 언어
    
    Returns:
        처리 결과 리스트
    """
    results = []
    
    for seg in segments_batch:
        try:
            result = model.generate(
                input=seg['audio'],
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
                results.append({
                    'success': True,
                    'start': seg['start'],
                    'end': seg['end'],
                    'text': clean_text
                })
            else:
                results.append({
                    'success': False,
                    'start': seg['start'],
                    'end': seg['end']
                })
        
        except Exception as e:
            results.append({
                'success': False,
                'start': seg['start'],
                'end': seg['end'],
                'error': str(e)[:100]
            })
    
    return results


def process_segments_threaded(model, segments, language, num_workers=None):
    """
    멀티스레딩으로 세그먼트를 병렬 처리
    
    Args:
        model: 사전 로드된 ASR 모델 (모든 스레드가 공유)
        segments: 처리할 세그먼트 리스트
        language: 대상 언어
        num_workers: 스레드 수 (None이면 CPU 코어의 70%)
    
    Returns:
        성공한 세그먼트 리스트 (시간순 정렬)
    """
    import multiprocessing as mp
    
    if num_workers is None:
        cpu_count = mp.cpu_count()
        num_workers = max(1, int(cpu_count * 0.7))
    
    print(f"\n⚡ 멀티스레드 병렬 처리 시작")
    print(f"   CPU 코어: {mp.cpu_count()}개")
    print(f"   스레드 수: {num_workers}개")
    print(f"   총 세그먼트: {len(segments)}개")
    print(f"   모델 공유: 단일 모델 인스턴스 사용")
    
    # 세그먼트를 배치로 나누기 (각 스레드가 여러 개씩 처리)
    batch_size = max(1, len(segments) // num_workers)
    batches = []
    for i in range(0, len(segments), batch_size):
        batches.append(segments[i:i + batch_size])
    
    print(f"   배치 수: {len(batches)}개 (배치당 ~{batch_size}개 세그먼트)")
    
    # ThreadPoolExecutor로 병렬 처리
    all_segments = []
    failed_count = 0
    completed_batches = 0
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # 모든 배치 제출
        future_to_batch = {
            executor.submit(process_segment_batch, model, batch, language): i
            for i, batch in enumerate(batches)
        }
        
        # 완료되는대로 결과 수집
        for future in as_completed(future_to_batch):
            batch_idx = future_to_batch[future]
            try:
                batch_results = future.result()
                for result in batch_results:
                    if result['success']:
                        all_segments.append({
                            'start': result['start'],
                            'end': result['end'],
                            'text': result['text']
                        })
                    else:
                        failed_count += 1
                        if 'error' in result:
                            print(f"  ⚠️  세그먼트 실패 [{result['start']:.1f}s-{result['end']:.1f}s]: {result.get('error', '')}")
                
                completed_batches += 1
                if completed_batches % 5 == 0 or completed_batches == len(batches):
                    print(f"  진행: {completed_batches}/{len(batches)} 배치 완료 ({completed_batches*100//len(batches)}%)")
            
            except Exception as e:
                print(f"  ❌ 배치 {batch_idx} 처리 실패: {str(e)[:100]}")
                failed_count += len(batches[batch_idx])
    
    # 시간순 정렬
    all_segments.sort(key=lambda x: x['start'])
    
    print(f"\n병렬 처리 완료!")
    print(f"  성공: {len(all_segments)}개")
    print(f"  실패: {failed_count}개")
    
    return all_segments
