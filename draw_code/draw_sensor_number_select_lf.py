# -*- encoding: UTF-8 -*-
'''
@File        : draw_sensor_number_select_lf.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-17 16:32:24
@Author      : tanxh 
'''

import matplotlib.pyplot as plt
import ast

data = {}
with open('./log/sensor_number_05-15_1.txt', 'r') as file:
    for line in file:
        parts = line.strip().split('\t\t')
        A, B, C, D = parts[0], parts[1], parts[2], parts[3]
        d_values = ast.literal_eval(D)

        data.update({(A, B, C):d_values})

selected_A = 'R3-P02D' # 选择机柜

selected_data_A = {key: value for key, value in data.items() if key[0] == selected_A}

# 创建画布
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(14, 12))
plt.subplots_adjust(wspace=0.4, hspace=0.5)  # 调整子图间距

plot_count = 0
plotted_combinations = set()

# 绘制图形
for position, data_List in selected_data_A.items():
    if plot_count >= 10:
        break  # 超过十张图则停止绘制

    lf, bname, sensor = position
    selected_bname = bname

    if (selected_A, selected_bname) in plotted_combinations:
        continue  # 已经绘制过该组合

    selected_data_bname = {key: value for key, value in selected_data_A.items() if key[1] == selected_bname}

    ax = axes[plot_count // 2, plot_count % 2]
    ax.set_title(f"({selected_A}, {selected_bname})", fontsize=10)
    for sensor_name, data in selected_data_bname.items():
        min_value = min(data)
        shifted_data = [value - min_value for value in data]  # 平移到最低值对齐
        ax.plot(range(len(data)), shifted_data, label=sensor_name[2])
    ax.set_xlabel("Index of window")
    ax.set_ylabel("Number of alarms")
    
    ax.set_xticks(range(0, len(data_List), 10))
    ax.set_xticklabels([f"{i * 10}" for i in range(len(data_List) // 10 + 1)], rotation=45, fontsize=6)
    ax.set_yticks(range(-3, 4))
    ax.set_yticks(range(0, max(shifted_data) + 1))  # 设置 y 轴刻度范围

    ax.legend(fontsize='x-small')

    plotted_combinations.add((selected_A, selected_bname))
    plot_count += 1

plt.tight_layout()

plt.show()




