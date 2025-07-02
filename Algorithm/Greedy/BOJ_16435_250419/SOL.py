import sys
sys.stdin = open('input.txt','r')  # 파일 입력 받기 (테스트용)

# 과일 개수와 스네이크버드의 초기 키 입력
fruit_num, snakebird_height = map(int, input().split())

# 과일 높이 리스트 입력 및 정렬 (낮은 나무부터 먹기 위해)
fruit_list = list(map(int, input().split()))
fruit_list.sort()

# 과일을 하나씩 확인하면서 조건에 맞게 먹기
for i in range(fruit_num):
    if snakebird_height >= fruit_list[i]:  # 먹을 수 있는 높이일 경우
        snakebird_height += 1  # 과일을 먹고 키 1 증가
    else:
        break  # 더 이상 먹을 수 없음

# 최종 키 출력
print(snakebird_height)
