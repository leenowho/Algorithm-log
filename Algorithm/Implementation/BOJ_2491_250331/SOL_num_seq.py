'''
0에서부터 9까지의 숫자로 이루어진 N개의 숫자가 나열된 수열이 있다. 그 수열 안에서 연속해서 커지거나(같은 것 포함), 혹은 연속해서 작아지는(같은 것 포함) 수열 중 가장 길이가 긴 것을 찾아내어 그 길이를 출력하는 프로그램을 작성하라.

예를 들어 수열 1, 2, 2, 4, 4, 5, 7, 7, 2 의 경우에는 1 ≤ 2 ≤ 2 ≤ 4 ≤ 4 ≤ 5 ≤ 7 ≤ 7 이 가장 긴 구간이 되므로 그 길이 8을 출력한다. 수열 4, 1, 3, 3, 2, 2, 9, 2, 3 의 경우에는 3 ≥ 3 ≥ 2 ≥ 2 가 가장 긴 구간이 되므로 그 길이 4를 출력한다. 또 1, 5, 3, 6, 4, 7, 1, 3, 2, 9, 5 의 경우에는 연속해서 커지거나 작아지는 수열의 길이가 3 이상인 경우가 없으므로 2를 출력하여야 한다.
'''
import sys
sys.stdin = open('input.txt', 'r')  # 테스트용 입력 파일

N = int(input())  # 수열의 길이
arr = list(map(int, input().split()))  # 수열 입력
arr_len = len(arr)

# 1. 비내림차순(≤) 탐색
max_val = 1  # 최대 길이 저장 변수
cnt = 1  # 현재 연속 길이

for i in range(arr_len - 1):
    if arr[i] <= arr[i + 1]:  # 다음 수가 크거나 같으면 연속
        cnt += 1
        if max_val < cnt:
            max_val = cnt
    else:
        cnt = 1  # 연속 끊기면 리셋

# 2. 비비등차순(≥) 탐색
max_val_2 = 1
cnt_2 = 1

for j in range(arr_len - 1):
    if arr[j] >= arr[j + 1]:  # 다음 수가 작거나 같으면 연속
        cnt_2 += 1
        if max_val_2 < cnt_2:
            max_val_2 = cnt_2
    else:
        cnt_2 = 1  # 연속 끊기면 리셋

# 둘 중 최대값 출력
print(max(max_val, max_val_2))
