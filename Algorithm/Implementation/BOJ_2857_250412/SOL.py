import sys
sys.stdin = open('input.txt','r')  # input.txt 파일로부터 입력 받기

# 5줄의 입력을 받아 2차원 리스트 생성
arr = [list(input().split()) for _ in range(5)]  # 각 줄을 리스트로 저장

stack = []  # FBI 요원의 줄 번호를 저장할 리스트

# 각 줄을 탐색하면서 "FBI" 포함 여부 확인
for i in range(5):  # 줄 수 만큼 반복
    for j in arr[i]:  # 해당 줄의 단어들 중에서
        if "FBI" in j:  # "FBI"가 포함되어 있다면
            stack.append(i + 1)  # 줄 번호(i는 0-based → +1)
            break  # 해당 줄에서 더 이상 탐색하지 않음

# 결과 출력
if stack:
    print(*stack)  # 공백으로 구분하여 출력
else:
    print("HE GOT AWAY!")  # 아무도 없을 경우
