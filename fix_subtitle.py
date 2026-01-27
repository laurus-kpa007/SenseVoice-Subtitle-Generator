"""
SenseVoice 자막 후처리 스크립트
메타데이터를 제거하고 깨끗한 자막으로 변환
"""
import re
import sys

def clean_sensevoice_text(text):
    """SenseVoice 메타데이터 제거"""
    # <|언어|>, <|감정|>, <|타입|> 등 메타데이터 제거
    text = re.sub(r'<\|[^|]+\|>', '', text)
    # <speaker_N> 제거
    text = re.sub(r'<speaker_\d+>\s*', '', text)
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text

def process_srt_file(input_file, output_file):
    """SRT 파일 처리"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 각 자막 블록 처리
    blocks = content.split('\n\n')
    cleaned_blocks = []

    for block in blocks:
        if not block.strip():
            continue

        lines = block.split('\n')
        if len(lines) >= 3:
            # 번호와 타임스탬프는 유지, 텍스트만 정리
            number = lines[0]
            timestamp = lines[1]
            text = ' '.join(lines[2:])

            # 텍스트 정리
            cleaned_text = clean_sensevoice_text(text)

            if cleaned_text:  # 텍스트가 있는 경우만
                cleaned_blocks.append(f"{number}\n{timestamp}\n{cleaned_text}")

    # 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(cleaned_blocks))

    print(f"처리 완료: {output_file}")
    print(f"총 {len(cleaned_blocks)}개 자막 블록")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python fix_subtitle.py <입력파일> [출력파일]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.srt', '_cleaned.srt')

    process_srt_file(input_file, output_file)
