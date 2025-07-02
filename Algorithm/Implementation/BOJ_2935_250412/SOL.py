import sys
sys.stdin = open('input.txt', 'r')  # 테스트용 입력 파일

arr = [input().split() for _ in range(3)]  # 세 줄을 리스트로 받음

num1 = int(arr[0][0])  # 첫 번째 숫자
op = arr[1][0]         # 연산자 (+ 또는 *)
num2 = int(arr[2][0])  # 두 번째 숫자

# 연산자에 따라 연산 수행
if op == '+':
    print(num1 + num2)
elif op == '*':
    print(num1 * num2)
