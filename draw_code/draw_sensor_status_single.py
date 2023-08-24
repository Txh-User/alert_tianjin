# -*- encoding: UTF-8 -*-
'''
@File        : draw_sensor_status_single.py
@Environment : 
@Description : 
@Time        : 2023-08-16 18:25:22
@Author      : tanxh 
'''

import ast
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 行索引和时间范围
selected_row_index = 5
start_time = '05:40:00'
end_time = '07:10:00'

# 读取txt数据
data = []
txt_file = './log/sensor_status.txt'
with open(txt_file, 'r') as file:
    for line in file:
        parts = line.strip().split('\t\t')
        a, b, c, d_values_str = parts[0], parts[1], parts[2], parts[3]
        d_values = ast.literal_eval(d_values_str)
        data.append((a, b, c, d_values))

selected_data = data[selected_row_index - 1]

# 创建画布
plt.figure(figsize=(12, 8))

time_line = [datetime.strptime(time_str, '%H:%M:%S') for time_str, _ in selected_data[3]]

# 添加时间范围内的数据
filtered_time_line = []
filtered_y_data = []
for time_str, d in selected_data[3]:
    if start_time <= time_str <= end_time:
        filtered_time_line.append(datetime.strptime(time_str, '%H:%M:%S'))
        filtered_y_data.append(d)

plt.plot(filtered_time_line, filtered_y_data, drawstyle='steps-post')

# 设置标题、x轴标签和y轴标签
line_label = f'({selected_data[0]}, {selected_data[1]}, {selected_data[2]})'
plt.title('Alarm frequency of {} in 2023-05-15'.format(line_label), fontdict={'size':14})
plt.xlabel('Time', fontdict={'size':14})
plt.ylabel('Status(1:d, 2:nc, 3:nr, 4:cr)', fontdict={'size':14})

# 设置x轴刻度和格式
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# 设置x轴刻度范围
x_min = datetime.strptime(start_time, '%H:%M:%S')
x_max = datetime.strptime(end_time, '%H:%M:%S')
plt.xlim(x_min, x_max)

# 设置刻度
plt.xticks(rotation=45)
plt.yticks(range(1, 5, 1))

plt.grid(True, linestyle='--', alpha=0.5)

plt.show()

