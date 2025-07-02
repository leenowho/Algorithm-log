import sys
sys.stdin = open('input.txt','r')

T = int(input())
 
for tc in range(1, T + 1):
    beom, word_len = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(beom)]
    res = 0
 
    for i in range(beom):
        cnt = 0
        for j in range(beom):
            if arr[i][j] == 1:
                cnt += 1
            if arr[i][j] ==0 or j==beom-1:
                if cnt == word_len :
                    res += 1
                cnt = 0
 
 
 
    for i in range(beom):
        cnt_2 = 0
        for j in range(beom):
            if arr[j][i] == 1:
                cnt_2 += 1
            if arr[j][i]==0 or j==beom-1:
                if cnt_2 == word_len:
                    res += 1
                cnt_2 = 0
 
    print(f"#{tc} {res}")