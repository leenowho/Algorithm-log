import sys
sys.stdin = open('input.txt','r')
#########################################

fruit_num,snakebird_height=map(int,input().split())
fruit_list = list(map(int,input().split()))
fruit_list.sort()
for i in range(fruit_num):
    if snakebird_height >= fruit_list[i]:
        snakebird_height+=1
    else:
        break
print(snakebird_height)