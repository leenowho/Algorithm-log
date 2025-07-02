import sys
sys.stdin = open('input.txt','r')

T = int(input())    # test_case 개수를 받아옴
for tc in range(1,T+1):
    arr_len,play = map(int,input().split())
    arr=[0]+list(map(int,input().split()))
    for _ in range(play):
        i,j=map(int,input().split())
 
        for k in range(1,j+1):
            #만약 arr[현재값+이동값]과arr[현재값-이동값]이 범위 안이면
            if 1 <= i+k <= arr_len and 1 <= i-k <= arr_len:
                if arr[i+k] == arr[i-k]:
                    if arr[i+k]==0:
                        arr[i+k]=1
                        arr[i-k]=1
                    else:
                        arr[i+k]=0
                        arr[i-k]=0
 
 
    print(f"#{tc}", *arr[1:])