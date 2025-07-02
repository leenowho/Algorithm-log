import sys
sys.stdin = open('input.txt','r')  # input.txt에서 입력을 받음 

T = int(input())  # 테스트 케이스 개수
for tc in range(1, T+1):
    N, M = map(int, input().split())  # N: 행 개수, M: 열 개수
    arr = [list(map(int, input().split())) for _ in range(N)]  # 2차원 배열 입력

    # 가로 방향에서 연속된 1의 최대 개수 찾기
    max_val_1 = 0
    for i in range(N):  # 모든 행을 탐색
        cnt_1 = 0
        for j in range(M):  # 열 순회
            if arr[i][j] == 1:
                cnt_1 += 1
                if cnt_1 > max_val_1:  # 최댓값 갱신
                    max_val_1 = cnt_1
            else:
                cnt_1 = 0  # 1이 끊기면 초기화

    # 세로 방향에서 연속된 1의 최대 개수 찾기
    max_val_2 = 0
    for i in range(M):  # 열을 기준으로
        cnt_2 = 0
        for j in range(N):  # 행 순회
            if arr[j][i] == 1:
                cnt_2 += 1
                if cnt_2 > max_val_2:
                    max_val_2 = cnt_2
            else:
                cnt_2 = 0

    # 출력 조건: 가로, 세로 모두 최대 연속 길이가 1이면 0 출력
    if max_val_1 == 1 and max_val_2 == 1:
        print(f"#{tc} {0}")
    else:
        print(f"#{tc} {max(max_val_1, max_val_2)}")  # 그 외에는 최댓값 출력
