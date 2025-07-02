import sys
sys.stdin = open('input.txt','r')  # input.txt에서 입력 받기

T = int(input())  # 테스트 케이스 개수
 
for tc in range(1, T + 1):
    beom, word_len = map(int, input().split())  # 배열 크기, 단어 길이
    arr = [list(map(int, input().split())) for _ in range(beom)]  # 2차원 배열 입력
    res = 0  # 정답 개수

    # 가로 방향 체크
    for i in range(beom):
        cnt = 0
        for j in range(beom):
            if arr[i][j] == 1:
                cnt += 1  # 연속된 1의 개수 누적
            if arr[i][j] == 0 or j == beom - 1:  # 벽이거나 마지막 열일 경우
                if cnt == word_len:  # 정확히 원하는 길이만 인정
                    res += 1
                cnt = 0  # 카운트 초기화
 
    # 세로 방향 체크
    for i in range(beom):
        cnt_2 = 0
        for j in range(beom):
            if arr[j][i] == 1:
                cnt_2 += 1
            if arr[j][i] == 0 or j == beom - 1:
                if cnt_2 == word_len:
                    res += 1
                cnt_2 = 0
 
    # 결과 출력
    print(f"#{tc} {res}")
