import sys
sys.stdin = open('input.txt', 'r')  # 테스트용 입력

n = input().strip()  # 문자열 입력 (양쪽 공백 제거)
result = ''  # 결과 문자열 초기화

# 'CAMBRIDGE'에 포함되지 않은 글자만 누적
for i in n:
    if i not in 'CAMBRIDGE':
        result += i

# 최종 결과 출력
print(result)
