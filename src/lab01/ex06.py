N = int(input("in_1: "))
och = 0
zaoch = 0
for i in range(N):
    data = input(f"in_{i+2}: ").split()
    form = data[-1]
    if form=='True':
        och+=1
    else:
        zaoch+=1
print(f"out: {och} {zaoch}")