N = int(input())
och = 0
zaoch = 0
for i in range(N):
    data = input().split()
    form = data[-1]
    if form=='True':
        och+=1
    else:
        zaoch+=1
print(f"in_1: ")
print(f"in_2: ")
print(f"in_3: ")
print(f"in_4: ")
print(f"out: {och} {zaoch}")