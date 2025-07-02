import sys
sys.stdin = open('input.txt','r')

T = int(input())    # test_case 개수를 받아옴
for tc in range(1,T+1):
    arr_len,play = map(int,input().split())
    arr=[0]+list(map(int,input().split()))
    for _ in range(play):
        i,j=map(int,input().split())
        base=arr[i]
        for k in range(j):
            if 1 <= i+k <= arr_len:
                arr[i+k] = base
    print(f"#{tc}", *arr[1:])
                                   