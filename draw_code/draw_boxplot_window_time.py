# -*- encoding: UTF-8 -*-
'''
@File        : draw_boxplot_window_time.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-11 12:58:44
@Author      : tanxh 
'''

import matplotlib.pyplot as plt
import numpy as np

file1 = "log/200alarm_process_time.txt"
file2 = "log/400alarm_process_time.txt"
file3 = "log/600alarm_process_time.txt"
file4 = "log/800alarm_process_time.txt"
file5 = "log/1000alarm_process_time.txt"

# 读取四个txt文件的数据
file_names = [file1, file2, file3, file4, file5]
data = []

for file_name in file_names:
    with open(file_name, 'r') as f:
        next(f)
        file_data = []
        for line in f:
            parts = line.strip().split('\t\t')
            index = int(parts[0])
            time = float(parts[1])
            file_data.append(time)
        data.append(file_data)

label = [200, 400, 600, 800, 1000]
# 设置箱型图参数
fig, ax = plt.subplots()
ax.boxplot(data, labels=label)

# 设置标签和标题
ax.set_xlabel('Number of Alerts', fontsize=16)
ax.set_ylabel('Process time for each number of alerts(ms)', fontsize=16)
ax.set_title('Boxplot of process time with different number of alerts', fontsize=16)

plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
