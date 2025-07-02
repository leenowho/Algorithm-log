import sys
sys.stdin = open('input.txt','r')  # input.txt에서 입력 받기 (테스트용)

Paper_gaesu = int(input())  # 색종이 개수

# 100x100 도화지를 101x101 배열로 생성 (인덱스 100까지 접근 가능)
arr = [[0] * 101 for _ in range(101)]

# 각 색종이 위치를 배열에 표시
for _ in range(Paper_gaesu):
    x, y = map(int, input().split())  # 색종이의 왼쪽 아래 꼭짓점 좌표
    for i in range(x, x + 10):  # 색종이 가로 범위 (10칸)
        for j in range(y, y + 10):  # 색종이 세로 범위 (10칸)
            arr[i][j] = 1  # 칠해진 칸을 1로 표시 (겹쳐도 1 그대로)

# 넓이 계산 (1로 칠해진 부분의 개수 세기)
result = 0
for i in arr:
    for j in i:
        if j == 1:
            result += 1

# 최종 넓이 출력
print(result)
