import sys
sys.stdin = open('input.txt','r')  # input.txt에서 입력 받기

T = int(input())  # 테스트 케이스 수

for tc in range(1, T + 1):
    mun_len, beom = map(int, input().split())  # 전체 문자열 길이, 검사할 부분 길이
    str_ = input()  # 문자열 입력

    result = None  # 회문 결과 초기화

    for i in range(mun_len - beom + 1):  # 가능한 시작 위치 범위
        str_dap = str_[i:i + beom]  # 부분 문자열 추출
        if str_dap == str_dap[::-1]:  # 회문인지 검사
            result = str_dap  # 정답 저장
            break  # 가장 먼저 찾은 회문만 출력

    if result:
        print(f"#{tc} {result}")
    else:
        print(f"#{tc} NONE")
