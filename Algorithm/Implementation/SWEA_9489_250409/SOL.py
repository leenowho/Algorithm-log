import sys
sys.stdin = open('input.txt','r')

T = int(input())  # 테스트 케이스 개수 입력 받기

for tc in range(1, T + 1):
    N, M = map(int, input().split())  # N: 행 수, M: 열 수
    arr = [list(map(int, input().split())) for _ in range(N)]  # 2차원 배열 입력 받기

    # 가장 긴 연속된 1의 개수를 구하는 문제
    # 가로 방향 먼저 탐색
    max_val_1 = -float("inf")  # 가로 방향 최댓값 초기화

    for i in range(N):  # 각 행에 대해
        cnt_1 = 0  # 연속된 1의 개수 카운트
        for j in range(M):  # 열을 순회하면서
            if arr[i][j] == 1:  # 1이면
                cnt_1 += 1  # 개수 증가
                if cnt_1 > max_val_1:  # 최댓값 갱신
                    max_val_1 = cnt_1
            else:  # 0이면 연속이 끊김
                cnt_1 = 0

    # 세로 방향 탐색
    max_val_2 = -float("inf")  # 세로 방향 최댓값 초기화

    for i in range(M):  # 각 열에 대해
        cnt_2 = 0  # 연속된 1의 개수 카운트
        for j in range(N):  # 행을 순회하면서
            if arr[j][i] == 1:  # 1이면
                cnt_2 += 1  # 개수 증가
                if cnt_2 > max_val_2:  # 최댓값 갱신
                    max_val_2 = cnt_2
            else:  # 0이면 연속이 끊김
                cnt_2 = 0

    # 가로/세로 중 가장 긴 연속 1의 길이 출력
    print(f"#{tc} {max(max_val_1, max_val_2)}")
