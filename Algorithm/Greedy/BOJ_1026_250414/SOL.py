import sys
sys.stdin = open('input.txt', 'r')  # input.txt에서 입력 받기 (테스트용)

N = int(input())  # 배열의 크기

# 배열 A와 B 입력 받기
a_arr = list(map(int, input().split()))
b_arr = list(map(int, input().split()))

result = 0  # 결과값 초기화

#  A는 오름차순 정렬, B는 내림차순 정렬
a_arr.sort()  # A: 가장 작은 값부터 곱할 수 있게 정렬
b_arr.sort(reverse=True)  # B: 가장 큰 값부터 곱할 수 있게 정렬

# 각 인덱스끼리 곱해서 누적합 계산
for i in range(N):
    result += a_arr[i] * b_arr[i]

# 결과 출력
print(result)
