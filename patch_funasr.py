"""
FunASR editdistance 패치 스크립트
editdistance를 python-Levenshtein으로 대체
"""

import os
import sys

def patch_funasr():
    """FunASR의 editdistance를 Levenshtein으로 패치"""

    # funasr 패키지 경로 찾기
    try:
        import funasr
        funasr_path = os.path.dirname(funasr.__file__)
        print(f"FunASR 경로: {funasr_path}")
    except ImportError:
        print("FunASR이 설치되지 않았습니다.")
        return False

    # editdistance를 사용하는 파일 찾기
    patched_count = 0

    for root, dirs, files in os.walk(funasr_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # editdistance import 확인
                    if 'import editdistance' in content or 'from editdistance' in content:
                        print(f"패치 중: {filepath}")

                        # editdistance를 Levenshtein으로 교체
                        new_content = content.replace(
                            'import editdistance',
                            'import Levenshtein as editdistance'
                        )
                        new_content = new_content.replace(
                            'from editdistance import',
                            'from Levenshtein import'
                        )

                        # editdistance.eval을 Levenshtein.distance로 교체
                        new_content = new_content.replace(
                            'editdistance.eval(',
                            'editdistance.distance('
                        )

                        # 파일 저장
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)

                        patched_count += 1
                        print(f"  ✓ 완료")

                except Exception as e:
                    print(f"  ✗ 오류: {e}")

    if patched_count > 0:
        print(f"\n총 {patched_count}개 파일 패치 완료!")
        return True
    else:
        print("\n패치할 파일이 없습니다.")
        return True

if __name__ == '__main__':
    success = patch_funasr()
    sys.exit(0 if success else 1)
