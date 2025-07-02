import sys
sys.stdin = open('input.txt','r')  # 테스트 입력 파일 열기

T = int(input())  # 테스트 케이스 수

for tc in range(1, T + 1):
    N = int(input())  # 스위치 개수
    start_switch = list(map(int, input().split()))  # 시작 상태
    target_switch = list(map(int, input().split()))  # 목표 상태

    result = 0  # 반전 횟수

    for i in range(N):
        if start_switch[i] != target_switch[i]:  # 다른 위치가 발견되면
            for j in range(i, N):  # 그 위치부터 끝까지 뒤집기
                start_switch[j] = 1 - start_switch[j]  # 0↔1 반전
            result += 1  # 연산 1회 추가

    print(f"#{tc} {result}")
