# -*- encoding: UTF-8 -*-
'''
@File        : split_by_period.py
@Environment : 
@Description : 
@Time        : 2023-08-13 23:39:01
@Author      : tanxh 
'''

import csv
import os
from datetime import datetime
from dateutil.parser import parser
from tqdm import tqdm

def splitByPeriod(input_file, output_file):
    # 初始化时间段字典
    time_periods = {
        (0, 8): '0-8',
        (8, 16): '8-16',
        (16, 24): '16-24'
    }

    # 初始化字典来存储每个时间段的数据
    data_by_period = {period_name: [] for period_name in time_periods.values()}

    # 打开CSV文件并按行读取数据
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # 跳过标题行
        for row in tqdm(csv_reader):
            if len(row) >= 6:  # 确保行有足够的列
                timestamp = row[11] # 第六列时间戳数据
                hour = int(timestamp[11:13])  # 获取小时部分

                # 查找对应的时间段
                target_period = None
                for period, period_name in time_periods.items():
                    start, end = period
                    if start <= hour < end:
                        target_period = period_name
                        break

                if target_period is not None:
                    data_by_period[target_period].append(row)

    # 将数据写入对应的文件
    for period_name, data_rows in tqdm(data_by_period.items()):
        file_path = os.path.join(output_file, f"{period_name}.csv")
        with open(file_path, 'w', newline='', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(header)  # 标题行
            csv_writer.writerows(data_rows)

    print("写入完成！")

def main():
    
    # 定义输入CSV文件和输出文件夹路径
    csv_filename = 'data/split_day_after/2023-01-28.csv'
    output_folder = 'data/split_period'

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    splitByPeriod(csv_filename, output_folder)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))