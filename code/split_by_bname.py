# -*- encoding: UTF-8 -*-
'''
@File        : split_by_bname.py
@Environment : TJalarm
@Description : split alarm data from each bname
@Time        : 2023-08-15 11:06:58
@Author      : tanxh 
'''

import os
import csv
from tqdm import tqdm

def splitByBname(input_file, output_file):
    file_data = {}

    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        for row in csv_reader:
            bname = row[1]
            lc = row[6]
            lf = row[7]
            position = (lc, lf, bname)

            if position not in file_data:
                file_data[position] = []
            file_data[position].append(row)

    for position, rows in tqdm(file_data.items(), desc='处理进度'):
        # split_bname/lcname/lfname/bname.csv

        file_path = os.path.join(output_file, position[0], position[1])
        os.makedirs(file_path, exist_ok=True)

        file_path += f'/{position[2]}.csv'

        with open(file_path, 'w', newline='', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(header)  # 写入标题行
            csv_writer.writerows(rows)

    print("文件划分完成！")

def main():
    csv_file_path = "./data/sensor-alarm-info_final.csv"
    save_path = "./data/split_bname_before"

    os.makedirs(save_path, exist_ok=True)

    print("目标文件：" + str(csv_file_path))

    splitByBname(csv_file_path, save_path)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("运行耗时：{:.4f}s".format(end_time - start_time))

