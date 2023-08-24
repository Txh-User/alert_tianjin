# -*- encoding: UTF-8 -*-
'''
@File        : chattering_iteration.py
@Environment : 
@Description : 
@Time        : 2023-08-16 11:27:25
@Author      : tanxh 
'''

import os
import csv
from tqdm import tqdm
from datetime import datetime, timedelta

def save_data(rule, path): # 保存结果到txt文件
    with open(path, "w") as f:
        f.write("index\tbefore\tafter\ttime\n")
        for iteration, item in rule.items():
            s = "{}\t\t{}\t\t{}\t\t{}\n".format(iteration, item[0][0], item[0][1], item[1])
            f.write(s)
        f.close()
    # print("正在写入：{}".format(path))

def find_data_in_position_dict(input_file, output_file, window_size_minutes, index):
    window_size = timedelta(minutes=window_size_minutes)
    result = []
    window_data = {}

    # print("窗口大小：{}".format(window_size))

    with open(input_file, 'r', newline='') as csvfile:
        # print("读取文件：{}".format(input_file))
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        prev_window_end = None
        positions_data = {}
        datalen = 0
        window_iteration = 1

        # print("solution2 正在计算…")
        for row in tqdm(list(reader)):
            datalen += 1
            timestamp = datetime.strptime(row['ctime'], '%Y-%m-%d %H:%M:%S')

            if not prev_window_end:
                # 初始化第一个窗口
                prev_window_end = timestamp + window_size

            if timestamp > prev_window_end:   
                # 当前数据时间戳超出窗口，处理前置窗口数据并重置窗口
                process_position_data(positions_data, result, window_data, window_iteration)

                window_iteration += 1
                positions_data = {}
                prev_window_end = timestamp + window_size

            # 将当前行的位置信息保存为一个元组，并将数据添加到字典对应位置的列表中
            position = (row['sid'], row['bname'], row['lf'])

            if position not in positions_data:
                positions_data[position] = []

            positions_data[position].append(row)

        # 处理最后一个窗口数据
        process_position_data(positions_data, result, window_data, window_iteration)

        print("第{}次迭代，原有 {} 行，剩余 {} 行，收敛率：{:.2f}%".format(index + 1, datalen, len(result), (1 - len(result) / datalen) * 100))

    # 写入文件
    # print("正在写入：{}".format(output_file))

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result)

    txtfolder = "log/chattering_iteration_log/"
    os.makedirs(txtfolder, exist_ok=True)

    txtpath = txtfolder + "{}min_iteration_{}.txt".format(window_size_minutes, index + 1)
    save_data(window_data, txtpath)

    # print("写入完成")

def process_position_data(positions_data, result, window_data, window_iteration):
    start_time = time.time()
    result_before = len(result)
    windowlen = 0

    for position, data in positions_data.items():
        windowlen += len(data)
        status_values = set(item['status'] for item in data)

        if ('nc' in status_values or 'nr' in status_values or 'cr' in status_values) and\
            ('dnc' in status_values or 'dnr' in status_values or 'dcr' in status_values):
            first_nc_data = next(item for item in data if item['status'][0] != 'd')
            last_dnc_data = next(item for item in reversed(data) if item['status'][0] == 'd')

            result.append(first_nc_data)
            result.append(last_dnc_data)

    result_after = len(result)

    end_time = time.time()
    runtime = (end_time - start_time) * 1000

    # 计算当前窗口收敛前后的行数与处理时间
    windowdata = (windowlen, result_after - result_before)
    window_data[window_iteration] = []
    window_data[window_iteration].append(windowdata)
    window_data[window_iteration].append(round(runtime, 5))

def main():
    # 窗口大小，单位：min
    window_size_minutes = 5

    print("窗口大小：{}min".format(window_size_minutes))

    for index in range(0, 5):

        csv_file_path = "data/chattering_iteration/{}min_iteration_{}.csv".format(window_size_minutes, index)
        save_path = "data/chattering_iteration/{}min_iteration_{}.csv".format(window_size_minutes, index + 1)

        # solution 2
        find_data_in_position_dict(csv_file_path, save_path, window_size_minutes, index)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("运行耗时：{:.4f}s".format(end_time - start_time))


