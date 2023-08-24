# -*- encoding: UTF-8 -*-
'''
@File        : split_by_lc.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-11 14:57:34
@Author      : tanxh 
'''

import csv
import os
from tqdm import tqdm

def splitByLc(input_file, output_file):
    # 字典用于存储每个文件的数据
    file_data = {}
    result = []

    # 打开CSV文件并按行读取数据
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # 跳过标题行

        for row in csv_reader:
            col_6_data = row[6]  # 第六列数据
            if col_6_data not in file_data:
                file_data[col_6_data] = []
            file_data[col_6_data].append(row)

    # 将数据写入对应的文件
    for col_6_data, rows in tqdm(file_data.items(), desc="处理进度", unit="文件"):
        file_path = os.path.join(output_file, f"{col_6_data}.csv")
        log_path = os.path.join(output_file, f'log.txt')

        with open(file_path, 'w', newline='', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(header)  # 写入标题行
            csv_writer.writerows(rows)

        s = "{}\t{}\n".format(col_6_data, len(rows))
        result.append(s)
        result.sort()

    for item in result:
        with open(log_path, "a") as f:
            f.write(item)
                

    print("文件划分完成！")

def main():
    csv_file_path = "data/sensor_positiondict_removed_5.csv"
    save_path = "data/split_lc"

    os.makedirs(save_path, exist_ok=True)

    print("目标文件：" + str(csv_file_path))

    splitByLc(csv_file_path, save_path)

# Call main()
if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))
