# -*- encoding: UTF-8 -*-
'''
@File        : alarm_data_process.py
@Environment : Time2State
@Description : 
@Time        : 2023-08-19 23:59:28
@Author      : tanxh 
'''

import pandas as pd
import os
import numpy as np
import csv
import datetime
from tqdm import tqdm

def txt_to_csv(input_file, output_file):
    txt_data = {}
    csv_data = []

    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t\t')
            time_status = parts[3]
            position = (parts[0], parts[1], parts[2])
            date_value_pairs = eval(time_status)

            if position not in txt_data:
                txt_data[position] = []
            txt_data[position].append(date_value_pairs)

    # 一天的秒数，设定起始时间，创建时间列表
    total_seconds_in_a_day = 24 * 60 * 60
    min_date = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
    csv_data = [0] * len(txt_data)

    data_line = 0
    for position, line in tqdm(txt_data.items(), desc="生成时序"):
        second = 0
        data = []
        data.append(position)
        for index, item in enumerate(line[0]):
            date = item[0]
            now_value = item[1]

            if index != 0:
                front_value = line[0][index - 1][1]
            else:
                front_value = now_value

            date = datetime.datetime.strptime(date, "%H:%M:%S")
            index = int((date - min_date).total_seconds())
            while(second < total_seconds_in_a_day):
                if(second == index):
                    data.append(now_value)
                    second += 1
                    break
                else:
                    data.append(front_value)
                    second += 1

            # 补全长度
        data = data + [now_value] * (total_seconds_in_a_day - len(data) + 1)

        csv_data[data_line] = data
        data_line += 1

    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for line in csv_data:
            csv_writer.writerow(line)

def main():
    txt_path = './log/sensor_status.txt'
    csv_path = './log/sensor_status.csv' # (644,86640)

    txt_to_csv(txt_path, csv_path)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("Run time: {:.4f}s".format(end_time - start_time))

    