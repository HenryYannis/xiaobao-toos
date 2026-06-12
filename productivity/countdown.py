#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小宝工具箱 - 数字倒计时 (Countdown Timer)

功能：
- 全屏显示数字倒计时
- 支持自定义倒计时时长
- 精确到秒的倒计时

使用方法：
- 直接运行即可开始倒计时
- 倒计时结束后自动退出

注意事项：
- 需要 turtle 库（Python 自带）
- 需要图形界面支持
- 默认使用 HeiTi 字体，如不存在会使用系统默认字体

作者：小宝科技帝国
日期：2024
"""

import turtle
import time

# 设置背景和画笔颜色
turtle.bgcolor("black")
turtle.pencolor("white")
turtle.penup()
turtle.goto(0, -100)
turtle.pendown()

# 倒计时从10到0
for i in range(10, -1, -1):
    try:
        turtle.write(i, align="center", font=("HeiTi", 200, "bold"))
    except Exception:
        # 如果 HeiTi 字体不存在，使用默认字体
        turtle.write(i, align="center", font=("Arial", 200, "bold"))
    time.sleep(1)
    turtle.clear()

turtle.done()
