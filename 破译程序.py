import random
import time

a = 0
while True:
    print(' '.join(random.choice([' ','1','0'])for i in range(73)))
    if a > 4000:
        print("正在破译中......")
        print("...")
        time.sleep(2)
        print("正在破译中......")
        print("...")
        time.sleep(2)
        print("正在破译中......")
        print("...")
        time.sleep(2)
        print("破译完成")
        print("请尽快阅读，10s后自动销毁")
        print("犀牛铁军即将入侵地球，请尽快做好战事准备 ———— 一位和平爱好者")
        time.sleep(10)
        break
    a += 1
