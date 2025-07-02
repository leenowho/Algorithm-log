import sys
sys.stdin = open('input.txt','r')
#########################################

n = int(input())
paper = [[0]*100 for _ in range(100)]

# 색종이 표시
for _ in range(n):
    x, y = map(int, input().split())
    for i in range(x, x+10):
        for j in range(y, y+10):
            paper[i][j] = 1

# 둘레 계산
perimeter = 0
for i in range(100):
    for j in range(100):
        if paper[i][j] == 1:
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + dx, j + dy
                # 범위를 벗어나거나 인접한 칸이 0이면 둘레 증가
                if not (0 <= ni < 100 and 0 <= nj < 100):
                    perimeter += 1
                elif paper[ni][nj] == 0:
                    perimeter += 1


print(perimeter)





