import sys
sys.stdin = open('input.txt', 'r')  # 테스트용 input 파일 열기

# 100x100 2차원 평면 생성 (최대 좌표값이 100 미만이므로 충분함)
arr = [[0] * 100 for _ in range(100)]

# 직사각형 4개 입력 처리
for i in range(4):
    left_x, left_y, right_x, right_y = map(int, input().split())
    
    # 각 직사각형의 내부 좌표를 1로 표시
    # 주의: 오른쪽, 위쪽 끝은 포함하지 않음 (open interval)
    for x in range(left_x, right_x):
        for y in range(left_y, right_y):
            arr[x][y] = 1  # 해당 영역을 덮음

# 넓이 계산 (1이 표시된 칸 수)
cnt = 0
for check in arr:
    for real in check:
        if real == 1:
            cnt += 1

# 정답 출력
print(cnt)
