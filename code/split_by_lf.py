# -*- encoding: UTF-8 -*-
'''
@File        : split_by_lf.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-16 10:33:03
@Author      : tanxh 
'''

import csv
import os
from tqdm import tqdm

def splitByLf(input_file, output_file):
    # 字典用于存储每个文件的数据
    file_data = {}

    # 打开CSV文件并按行读取数据
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # 跳过标题行

        for row in csv_reader:
            lc = row[6]
            lf = row[7]
            position = (lc, lf)

            if position not in file_data:
                file_data[position] = []
            file_data[position].append(row)

    # 将数据写入对应的文件
    for position, rows in tqdm(file_data.items(), desc="处理进度"):
        # split_lf/lc/lf.csv

        file_path = os.path.join(output_file, position[0])
        os.makedirs(file_path, exist_ok=True)
        file_path += f'/{position[1]}.csv'

        with open(file_path, 'w', newline='', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(header)  # 写入标题行
            csv_writer.writerows(rows)

    print("文件划分完成！")

def main():
    csv_file_path = "data/sensor_positiondict_removed_5.csv"
    save_path = "data/split_lf"

    os.makedirs(save_path, exist_ok=True)

    print("目标文件：" + str(csv_file_path))

    splitByLf(csv_file_path, save_path)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("运行耗时：{:.4f}s".format(end_time - start_time))