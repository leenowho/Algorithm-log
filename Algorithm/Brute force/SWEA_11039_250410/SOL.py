import sys
sys.stdin = open('input.txt','r')

T = int(input())    # test_case 개수를 받아옴
 
for tc in range(1, T+1) :
    n=int(input())
    arr=[list(map(int,input().split())) for _ in range(n)]
 
    stack=[]
 
    for i in range(n):
        cnt_1=0
        for j in range(n):
            if arr[i][j]==1:
                cnt_1+=1
            else:
                cnt_1=0
            cnt_2 = 0
 
            for O in range(n):
                if arr[O][j] == 1:
                    cnt_2 += 1
                else:
                    cnt_2 = 0
                stack.append(cnt_1*cnt_2)
 
    print(f"#{tc} {max(stack)}")