import sys
sys.stdin = open('input.txt','r')  # 테스트 파일 입력

# '+' 방향(상하좌우)으로 폭탄 퍼짐을 계산하는 함수
def gaseo(N, M, arr):
    dic = [(0,1), (0,-1), (1,0), (-1,0)]  # 우, 좌, 하, 상
    for i in range(N):
        for j in range(N):
            temp = arr[i][j]  # 현재 위치의 값 포함
            for nx, ny in dic:  # 각 방향에 대해
                for k in range(1, M):  # M-1 칸까지 퍼짐
                    ni = i + nx * k
                    nj = j + ny * k
                    if not (0 <= ni < N and 0 <= nj < N):  # 범위 밖이면 무시
                        continue
                    temp += arr[ni][nj]
            stack.append(temp)  # 해당 위치에서의 total 값 저장

# 'X' 방향(대각선)으로 폭탄 퍼짐을 계산하는 함수
def dae(N, M, arr):
    dic = [(1,1), (-1,-1), (1,-1), (-1,1)]  # 우하, 좌상, 좌하, 우상
    for i in range(N):
        for j in range(N):
            temp = arr[i][j]  # 현재 위치의 값 포함
            for nx, ny in dic:  # 각 대각선 방향에 대해
                for k in range(1, M):  # M-1 칸까지 퍼짐
                    ni = i + nx * k
                    nj = j + ny * k
                    if not (0 <= ni < N and 0 <= nj < N):  # 범위 밖이면 무시
                        continue
                    temp += arr[ni][nj]
            stack.append(temp)  # 해당 위치에서의 total 값 저장

T = int(input())  # 테스트 케이스 개수
for tc in range(1, T+1):
    N, M = map(int, input().split())  # 배열 크기 N, 폭탄 범위 M
    arr = [list(map(int, input().split())) for _ in range(N)]  # 2차원 배열 입력

    stack = []  # 가능한 모든 총합을 저장할 리스트
    result_1 = gaseo(N, M, arr)  # '+' 방향 처리
    result_2 = dae(N, M, arr)  # 'X' 방향 처리

    print(f"#{tc} {max(stack)}")  # 가능한 모든 합 중 최대값 출력
