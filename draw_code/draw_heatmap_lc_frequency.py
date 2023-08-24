# -*- encoding: UTF-8 -*-
'''
@File        : draw_heatmap_lc_frequency.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-11 16:24:27
@Author      : tanxh 
'''

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# 从CSV文件中读取数据
data = []
with open('data/split_month/2023-03.csv', 'r') as csvfile:  # 替换为实际的文件路径
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # 跳过标题行
    for row in csv_reader:
        position = row[6]
        date = row[11][:10]
        data.append((position, date))

# 将数据按日期和位置进行统计
date_position_frequency = {}
positions = set()
for position, date in data:
    positions.add(position)
    if date not in date_position_frequency:
        date_position_frequency[date] = {}
    if position not in date_position_frequency[date]:
        date_position_frequency[date][position] = 0
    date_position_frequency[date][position] += 1

# 提取日期和位置数据以及对应的频率
dates = sorted(date_position_frequency.keys())
position_list = sorted(positions)
frequency_matrix = np.zeros((len(dates), len(position_list)))
for i, date in enumerate(dates):
    for j, position in enumerate(position_list):
        if position in date_position_frequency[date]:
            frequency_matrix[i, j] = date_position_frequency[date][position]

# 创建热图
fig, ax = plt.subplots()
cax = ax.matshow(frequency_matrix, cmap='viridis')

# 设置X轴和Y轴刻度标签
ax.set_xticks(np.arange(len(position_list)))
ax.set_yticks(np.arange(len(dates)))
ax.set_xticklabels(position_list, rotation=45, fontsize=6)
ax.set_yticklabels(dates, rotation=45, fontsize=6)

# 添加颜色带
cbar = plt.colorbar(cax)
cbar.ax.set_ylabel('Frequency', fontsize=14)

# 在热图中显示频率数值
for i in range(len(dates)):
    for j in range(len(position_list)):
        text = ax.text(j, i, f'{int(frequency_matrix[i, j])}', ha='center', va='center', color='w', fontsize=6)

# 设置图标题
ax.set_title('Heatmap of frequncy of lc', fontsize=14)

plt.tight_layout()
plt.show()


