import sys
sys.stdin = open('input.txt','r')
#########################################

input = sys.stdin.readline

#  8-넘버 생성
eight_numbers = [int('8' * i) for i in range(1, 19)]

#  가능한 합 저장
lucky = set()
current = set(eight_numbers)  # 1개 사용 시

for _ in range(7):  # 최대 8개까지 사용
    next_set = set()
    for total in current:
        for e in eight_numbers:
            new_sum = total + e
            next_set.add(new_sum)
    lucky.update(current)
    current = next_set
lucky.update(current)  # 마지막도 포함

#  입력 처리
T = int(input())
for _ in range(T):
    N = int(input())
    print("Yes" if N in lucky else "No")
