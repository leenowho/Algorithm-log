import sys
sys.stdin = open('input.txt','r')
T = int(input())    # test_case 개수를 받아옴
 
for tc in range(1, T+1) :
    n=int(input())
    arr=[list(map(int,input().split())) for _ in range(n)]
    result=[]
    dic=[(1,0),(-1,0),(0,1),(0,-1)]
    for i in range(n):
        for j in range(n):
            temp=arr[i][j]
            for dx,dy in dic:
                for o in range(1,n+1):
                    nx=i+dx*o
                    ny=j+dy*o
                    if not (0<=nx<n and 0<=ny<n):
                        continue
                    temp+=arr[nx][ny]
            result.append(temp)
 
    print(f"#{tc} {max(result)-min(result)}")