# -*- encoding: UTF-8 -*-
'''
@File        : draw_windowsize_time.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-10 15:48:26
@Author      : tanxh 
'''

import matplotlib.pyplot as plt
import numpy as np

data = []
with open('data/aggreration_lines.txt', 'r') as f:
    next(f)  # 跳过第一行（表头）
    for line in f.readlines()[:1000]:
        parts = line.strip().split('\t\t')
        before = int(parts[1])
        time = float(parts[3])
        data.append((before, time))  # 只保存 before 和 time

# 提取数据
before_values = [entry[0] for entry in data]
time_values = [entry[1] for entry in data]

# 绘制散点图
plt.scatter(before_values, time_values, marker='o')

# 设置标签和标题
plt.xlabel('#Alerts per window', fontsize=16)
plt.ylabel('Time(ms)', fontsize=16)

plt.tight_layout()
plt.show()





