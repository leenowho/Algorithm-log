import sys
sys.stdin = open('input.txt','r')  # 테스트용 input.txt

T = int(input())  # 테스트 케이스 수

for tc in range(1, T + 1):
    arr_len = int(input())  # 수열의 길이
    arr = list(map(int, input().split()))  # 수열 입력

    result = 1  # 가장 긴 오름차순 구간 길이
    cnt = 1     # 현재 연속 오름차순 길이

    for i in range(arr_len - 1):
        if arr[i] < arr[i + 1]:  # 다음 숫자가 더 크면 증가 구간
            cnt += 1
            if cnt > result:
                result = cnt  # 최댓값 갱신
        else:
            cnt = 1  # 오름차순이 끊기면 초기화

    print(f"#{tc} {result}")  # 결과 출력
