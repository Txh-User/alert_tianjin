# -*- encoding: UTF-8 -*-
'''
@File        : draw.py
@Environment : 
@Description : 
@Time        : 2023-08-02 11:14:07
@Author      : tanxh 
'''

import matplotlib.pylab as plt

#设置坐标轴
x = ["solution 1", "solution 2"]
y_20 = [3550316, 3550316]
y_21 = [274357, 263954]
y_22 = [208410, 199962]

bar_width = 0.2
x_20 = list(range(len(x)))
x_21 = [i + bar_width for i in x_20]
x_22 = [i + bar_width * 2 for i in x_20]

#设置大小
plt.figure(figsize=(14, 10), dpi=80)

#绘制
bar1 = plt.bar(range(len(x)), y_20, width=bar_width, label="raw data")
bar2 = plt.bar(x_21, y_21, width=bar_width, label="5min")
bar3 = plt.bar(x_22, y_22, width=bar_width, label="10min")

plt.bar_label(bar1)
plt.bar_label(bar2)
plt.bar_label(bar3)

#设置坐标信息
plt.xticks(x_21, x, fontsize=16)

plt.ylabel("alarm number/lines", fontsize=16)
plt.title("chattering alarm aggregation", fontsize=16)

#绘制图例
plt.legend()

#显示
plt.show()




# import matplotlib.pyplot as plt
# import numpy as np

# # 自定义函数，用于添加百分比标注
# def add_percentage_labels(ax):
#     for rect in ax.patches:
#         height = rect.get_height()
#         ax.annotate('{:.1f}%'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')

# # 提供示例数据，每三个数据为一组
# data = [30, 40, 50, 20, 10, 5, 15, 25, 35, 60, 70, 80]

# # 将数据分组，每三个数据为一组
# grouped_data = [data[i:i+3] for i in range(0, len(data), 3)]

# # 绘制柱形图
# fig, ax = plt.subplots()
# bar_width = 0.2
# index = np.arange(len(grouped_data[0]))

# # 绘制每组数据的柱形图
# for i, group in enumerate(grouped_data):
#     bar_positions = index + bar_width * i
#     ax.bar(bar_positions, group, bar_width, label='Group {}'.format(i + 1))

# # 添加图例
# ax.legend()

# # 添加百分比标注
# add_percentage_labels(ax)

# # 设置x轴标签和标题
# ax.set_xlabel('Data')
# ax.set_ylabel('Value')
# ax.set_title('Bar Chart with Percentage Labels')

# # 设置x轴刻度
# ax.set_xticks(index + bar_width * (len(grouped_data) - 1) / 2)
# ax.set_xticklabels(['Data 1', 'Data 2', 'Data 3'])

# plt.show()

