import sys
sys.stdin = open('input.txt','r')  # 파일 입력 처리 (테스트용)
input = sys.stdin.readline  # 빠른 입력 처리

# 1~18자리까지 '8'로 구성된 수 생성
eight_numbers = [int('8' * i) for i in range(1, 19)]

# 만들 수 있는 숫자들의 집합
lucky = set()
current = set(eight_numbers)  # 처음은 1개 사용 시 만들 수 있는 수

# 최대 8개의 숫자를 사용할 수 있음
for _ in range(7):  # 이미 1개 사용한 상태라 7번 반복
    next_set = set()
    for total in current:
        for e in eight_numbers:
            new_sum = total + e
            next_set.add(new_sum)  # 새로 만든 수 추가
    lucky.update(current)  # 현재까지의 조합 추가
    current = next_set  # 다음 단계로 진행

lucky.update(current)  # 마지막 집합도 포함

# 테스트 케이스 수 입력
T = int(input())
for _ in range(T):
    N = int(input())
    print("Yes" if N in lucky else "No")  # 만들 수 있으면 Yes, 아니면 No
