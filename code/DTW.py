# -*- encoding: UTF-8 -*-
'''
@File        : DTW.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-18 22:20:08
@Author      : tanxh 
'''

import ast
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np

def dtw_distance(x, y):
    # 获取两个序列的长度
    n = len(x)
    m = len(y)
    
    # 创建一个二维数组来存储DTW距离
    dtw_matrix = np.zeros((n + 1, m + 1))
    
    # 初始化第一行和第一列
    for i in range(1, n + 1):
        dtw_matrix[i][0] = float('inf')
    for j in range(1, m + 1):
        dtw_matrix[0][j] = float('inf')
    dtw_matrix[0][0] = 0
    
    # 填充DTW矩阵
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(x[i - 1] - y[j - 1])  # 计算两个数据点之间的距离
            dtw_matrix[i][j] = cost + min(dtw_matrix[i - 1][j], dtw_matrix[i][j - 1], dtw_matrix[i - 1][j - 1])
    
    # 返回DTW距离
    return dtw_matrix[n][m]

def main():
    with open('./log/sensor_number.txt', 'r') as file:
        lines = file.readlines()

    selected_line_numbers = [94, 93] # 选择所需序列的行号
    data = []
    position = []

    for line_number in selected_line_numbers:
        line = lines[line_number - 1]
        parts = line.strip().split('\t\t')
        data_value = ast.literal_eval(parts[3])
        positions = (parts[0], parts[1], parts[2])
        data.append(data_value)
        position.append(positions)

    print("比较序列：{}, {}".format(position[0],position[1]))

    x = np.array(data[0])
    y = np.array(data[1])

    distance = dtw_distance(x, y)
    print("DTW Distance:", distance)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("Run time: {:.4f}s".format(end_time - start_time))