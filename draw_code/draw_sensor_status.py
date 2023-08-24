# -*- encoding: UTF-8 -*-
'''
@File        : draw_sensor_status.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-16 15:38:06
@Author      : tanxh 
'''

import csv
import matplotlib.pyplot as plt
from datetime import datetime

i = 0
j = 10
selected_indices = [k for k in range(10)]

start_time = "00:00:00"
end_time = "23:59:59"

# 将自定义时间转换成秒
start_time_obj = datetime.strptime(start_time, "%H:%M:%S")
end_time_obj = datetime.strptime(end_time, "%H:%M:%S")

start_seconds = (start_time_obj - datetime(1900, 1, 1)).total_seconds()
end_seconds = (end_time_obj - datetime(1900, 1, 1)).total_seconds()

csvdata = []
with open('./log/sensor_status.csv', 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        csvdata.append(row)

# 创建子图网格
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 12))

# 绘制每个数据行的折线图
for i, index in enumerate(selected_indices):
    row = i % 5
    col = i // 5
    ax = axes[row, col]

    # 选择特定行的数据
    chosen_data = csvdata[index]

    time_steps = range(len(chosen_data) - 1)

    y_data = chosen_data[int(start_seconds) + 1:int(end_seconds) + 1]
    x_data = time_steps[int(start_seconds):int(end_seconds)]

    # 绘制折线图
    ax.plot(x_data, y_data, drawstyle='steps-post', label=chosen_data[0])
    # ax.set_xlabel('Time')
    ax.set_ylabel('Status')

    # 设置x轴范围为从开始时间到结束时间对应的秒数
    start_time_sec = int(start_time.split(':')[0]) * 3600 + int(start_time.split(':')[1]) * 60 + int(start_time.split(':')[2])
    end_time_sec = int(end_time.split(':')[0]) * 3600 + int(end_time.split(':')[1]) * 60 + int(end_time.split(':')[2])
    ax.set_xlim(start_time_sec, end_time_sec)

    # 设置x轴刻度为每小时一格
    x_ticks = range(start_time_sec, end_time_sec + 1, 3600)
    x_ticklabels = [f'{hour:02}:00' for hour in range(int(start_time.split(':')[0]), int(end_time.split(':')[0]) + 1)]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticklabels, rotation=45, ha='right', fontsize=8)

    ax.set_yticks(range(0, 4, 1))
    ax.set_yticklabels(range(1, 5, 1))

    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)


# 调整子图之间的间距
plt.tight_layout()

# 显示图像
plt.show()