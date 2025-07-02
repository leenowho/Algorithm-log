import sys
sys.stdin = open('input.txt','r')  # input.txt 파일에서 입력 받기

T = int(input())  # 테스트 케이스 개수

for tc in range(1, T + 1):
    arr_len, play = map(int, input().split())  # 배열 길이, 명령 횟수
    arr = [0] + list(map(int, input().split()))  # 1-indexed 배열 생성

    for _ in range(play):  # 명령 수행
        i, j = map(int, input().split())  # 기준 위치 i, 범위 j

        for k in range(1, j + 1):  # 대칭 거리 1~j까지 확인
            # 양쪽 인덱스가 배열 범위 내에 있을 경우
            if 1 <= i + k <= arr_len and 1 <= i - k <= arr_len:
                # 양쪽 값이 같으면 토글
                if arr[i + k] == arr[i - k]:
                    if arr[i + k] == 0:
                        arr[i + k] = 1
                        arr[i - k] = 1
                    else:
                        arr[i + k] = 0
                        arr[i - k] = 0

    # 결과 출력 (0번 인덱스는 제외)
    print(f"#{tc}", *arr[1:])
