import time
进度条 = 10
print("---------开始执行---------")
for i in range(进度条+1):
    a="**"*i
    b=".."*(进度条-i)
    c=(i/进度条)*100
    print(f"\r{c}%：[{a}->{b}]", end="", flush=True)
    time.sleep(1)
print("\n---------结束执行---------")