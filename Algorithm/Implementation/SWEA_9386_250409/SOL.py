import sys
sys.stdin = open('input.txt','r')
#########################################

T = int(input())  #  테스트 케이스 개수를 입력받음

for tc in range(1, T + 1):
    n_len = int(input())  #  숫자 문자열의 길이 (실제론 없어도 무방하나, 조건 상 포함됨)
    num = input()  #  문자열로 숫자 입력 (예: '1100111110')

    cnt = 0  #  현재 연속된 '1'의 개수
    max_1 = -float("inf")  #  최대 연속된 '1' 개수를 저장하기 위한 변수 (초기값은 아주 작은 수)

    for i in num:
        if i == '1':  #  '1'이 나오면
            cnt += 1  # 연속 카운트 증가
            if cnt > max_1:
                max_1 = cnt  # 지금까지 최대값보다 크면 갱신
        else:
            cnt = 0  #  '1'이 아닌 문자가 나오면 연속 카운트 초기화

    print(f"#{tc} {max_1}")  # 🖨 결과 출력
