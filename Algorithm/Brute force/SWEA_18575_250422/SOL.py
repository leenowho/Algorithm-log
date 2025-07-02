import sys
sys.stdin = open('input.txt','r')  # input.txt에서 입력 받기 (테스트용)

T = int(input())  # 테스트 케이스 개수

for tc in range(1, T + 1):
    n = int(input())  # 배열 크기 입력
    arr = [list(map(int, input().split())) for _ in range(n)]  # 2차원 배열 입력

    result = []  # 각 칸에서의 누적합을 저장할 리스트

    # 상하좌우 방향 설정
    dic = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):  # 모든 행에 대해
        for j in range(n):  # 모든 열에 대해
            temp = arr[i][j]  # 현재 위치의 값을 먼저 더함

            for dx, dy in dic:  # 상하좌우 4방향에 대해
                for o in range(1, n + 1):  # 1부터 n까지 거리
                    nx = i + dx * o
                    ny = j + dy * o

                    # 인덱스 범위 벗어나면 무시
                    if not (0 <= nx < n and 0 <= ny < n):
                        continue

                    # 유효한 범위면 누적 합에 포함
                    temp += arr[nx][ny]

            result.append(temp)  # 해당 위치에서 계산한 누적합 저장

    # 모든 위치에서의 누적합 중 최대값 - 최소값 출력
    print(f"#{tc} {max(result) - min(result)}")
