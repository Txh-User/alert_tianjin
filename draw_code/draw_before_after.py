# -*- encoding: UTF-8 -*-
'''
@File        : draw_before_after.py
@Environment : 
@Description : 
@Time        : 2023-08-10 15:49:17
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

plt.ylabel("alarm lines", fontsize=16)
plt.title("chattering alarm aggregation", fontsize=16)

#绘制图例
plt.legend()

#显示
plt.show()