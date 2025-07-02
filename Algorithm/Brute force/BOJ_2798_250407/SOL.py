import sys
sys.stdin = open('input.txt', 'r')  # 파일에서 입력 받기 (테스트 용도)

# 카드 개수(card_gaesu), 제한 값(limit) 입력 받기
card_gaesu, limit = map(int, input().split())

# 카드 종류 리스트 입력 받기
card_jongru = list(map(int, input().split()))

# 가능한 카드 조합의 합을 저장할 리스트
stack = []

# 세 장의 카드를 고르는 모든 조합을 확인 (완전 탐색)
for i in range(card_gaesu):
    for j in range(i + 1, card_gaesu):
        for k in range(j + 1, card_gaesu):
            # 카드 3장의 합이 limit 이하일 때만 저장
            total = card_jongru[i] + card_jongru[j] + card_jongru[k]
            if total <= limit:
                stack.append(total)

# 조건을 만족하는 조합들 중 가장 큰 합을 출력
print(max(stack))
