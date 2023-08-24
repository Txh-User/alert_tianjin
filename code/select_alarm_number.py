# -*- encoding: UTF-8 -*-
'''
@File        : select_alarm_number.py
@Environment : TJalarm
@Description : select a fix number of alarm to draw 
@Time        : 2023-08-11 10:47:49
@Author      : tanxh 
'''

import os
import csv
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path

def save_data(rule, path): # 保存结果到txt文件
    with open(path, "w") as f:
        f.write("index\tprocesstime\n")
        for iteration, item in rule.items():
            s = "{}\t\t{}\n".format(iteration, item[1])
            f.write(s)
        f.close()
    print("正在写入：{}".format(path))

def find_fix_number_alarm(input_file, output_file, alarm_num):
    result = []
    window_data = {}

    print("选取告警量：{}".format(alarm_num))

    with open(input_file, 'r', newline='') as csvfile:
        print("读取文件：{}".format(input_file))

        reader = csv.reader(csvfile)
        header = next(reader)

        positions_data = {}
        data_end = None
        datalen = 0
        window_iteration = 1

        print("正在计算…")
        for row in tqdm(list(reader)):
            datalen += 1

            if datalen > alarm_num * 100:
                break

            if not data_end:
                data_end = alarm_num

            if datalen > data_end:
                process_position_data(positions_data, result, window_data, window_iteration)

                window_iteration += 1
                positions_data = {}
                data_end += alarm_num

            # 将当前行的位置信息保存为一个元组，并将数据添加到字典对应位置的列表中
            position = (row[0], row[1], row[7])

            if position not in positions_data:
                positions_data[position] = []

            positions_data[position].append(row)

        process_position_data(positions_data, result, window_data, window_iteration)

    save_data(window_data, output_file)

def process_position_data(positions_data, result, window_data, window_iteration):
    start_time = time.time()
    windowlen = 0

    for position, data in positions_data.items():
        windowlen += len(data)
        status_values = set(item[10] for item in data)

        if ('nc' in status_values or 'nr' in status_values or 'cr' in status_values) and\
            ('dnc' in status_values or 'dnr' in status_values or 'dcr' in status_values):
            first_nc_data = next(item for item in data if item[10][0] != 'd')
            last_dnc_data = next(item for item in reversed(data) if item[10][0] == 'd')

            result.append(first_nc_data)
            result.append(last_dnc_data)

    end_time = time.time()
    runtime = (end_time - start_time) * 1000 # （ms）
    # 计算当前窗口收敛前后的行数
    window_data[window_iteration] = []
    window_data[window_iteration].append(windowlen)
    window_data[window_iteration].append(round(runtime, 5))

def main():
    fix_size = 1000

    csv_file_path = "data/sensor-alarm-info_final.csv"
    save_path = "log/{}alarm_process_time.txt".format(fix_size)

    find_fix_number_alarm(csv_file_path, save_path, fix_size)

# Call main()
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))