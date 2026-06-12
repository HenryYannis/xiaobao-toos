#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小宝工具箱 - 黑客帝国数字雨特效 (Hacker Matrix Digital Rain)

功能：
- 经典《黑客帝国》绿色数字雨特效
- 支持全屏显示
- 可作为屏幕保护程序使用

使用方法：
- 直接运行即可启动特效
- 按 Escape 键或关闭窗口退出

注意事项：
- 需要安装 pygame 库：pip install pygame
- 默认使用 SimHei 字体，如不存在会使用系统默认字体

作者：小宝科技帝国
日期：2024
"""

import random
import pygame

PANEL_width = 1800
PANEL_highly = 1000
FONT_PX = 15

pygame.init()

# 创建一个可视窗口
winSur = pygame.display.set_mode((PANEL_width, PANEL_highly))

font = pygame.font.SysFont('SimHei', 22)

bg_suface = pygame.Surface((PANEL_width, PANEL_highly), flags=pygame.SRCALPHA)
bg_suface = bg_suface.convert_alpha()

bg_suface.fill(pygame.Color(0, 0, 0, 28))

winSur.fill((0, 0, 0))

# 数字版
texts = [font.render(str(i), True, (0, 255, 0)) for i in range(2)]

# 字母版
# letter = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
#           'v', 'b', 'n', 'm']
# texts = [
#     font.render(str(letter[i]), True, (0, 255, 0)) for i in range(26)
# ]

# 按屏幕的宽带计算可以在画板上放几列坐标并生成一个列表
column = int(PANEL_width / FONT_PX)
drops = [0 for i in range(column)]

while True:
    # 从队列中获取事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:

            chang = pygame.key.get_pressed()
            if (chang[32]):
                exit()

    # 将暂停一段给定的毫秒数
    pygame.time.delay(30)

    # 重新编辑图像第二个参数是坐上角坐标
    winSur.blit(bg_suface, (0, 0))

    for i in range(len(drops)):
        text = random.choice(texts)

        # 重新编辑每个坐标点的图像
        winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))

        drops[i] += 1
        if drops[i] * 10 > PANEL_highly or random.random() > 0.95:
            drops[i] = 0

    pygame.display.flip()