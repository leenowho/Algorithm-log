import sys
sys.stdin = open('input.txt','r')  # 테스트용 입력 파일 열기

T = int(input())  # 테스트 케이스 수

for tc in range(1, T + 1):
    arr_len, play = map(int, input().split())  # 배열 길이, 플레이 수

    arr = [0] + list(map(int, input().split()))  # 1-based 인덱스를 위해 0 추가

    for _ in range(play):  # 플레이 수만큼 명령 수행
        i, j = map(int, input().split())  # i부터 시작해서 j개의 구간을 덮음
        base = arr[i]  # 기준값 저장
        for k in range(j):  # j개의 칸을 순회
            if 1 <= i + k <= arr_len:  # 배열 범위 체크
                arr[i + k] = base  # 값 덮어쓰기

    # 결과 출력 (0번 인덱스는 제외)
    print(f"#{tc}", *arr[1:])
