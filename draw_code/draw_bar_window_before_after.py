# -*- encoding: UTF-8 -*-
'''
@File        : draw_window_before_after.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-02 11:14:07
@Author      : tanxh 
'''

import matplotlib.pyplot as plt
import numpy as np

# 读取数据文件并提取前40行数据（跳过第一行）
data = []
with open('./log/aggreration_lines.txt', 'r') as f:
    next(f)  # 跳过第一行（表头）
    for line in f.readlines()[:60]:
        parts = line.strip().split('\t\t')
        index = int(parts[0])
        before = int(parts[1])
        after = int(parts[2])
        data.append((index, before, after))

# 提取数据
indices = [entry[0] for entry in data]
before_values = [entry[1] for entry in data]
after_values = [entry[2] for entry in data]

# 设置柱形图参数
bar_width = 0.35
x = np.arange(len(indices))

# 绘制柱形图
fig, ax = plt.subplots()
before_bars = ax.bar(x, before_values, bar_width, label='Before')
after_bars = ax.bar(x + bar_width, after_values, bar_width, label='After')

# 设置 x 轴的标注以每 5 个 index 划分
x_labels = [str(index) if index % 5 == 0 else '' for index in indices]
ax.set_xticks(x + bar_width / 2)
ax.set_xticklabels(x_labels)

# 设置标签和标题
ax.set_xlabel('#Window', fontsize=16)
ax.set_ylabel('#Alerts', fontsize=16)
ax.legend()

plt.tight_layout()
plt.show()

