# -*- encoding: UTF-8 -*-
'''
@File        : split_by_month.py
@Environment : 
@Description : 
@Time        : 2023/07/09 14:42:18
@Author      : tanxh 
'''

import csv
import os
from tqdm import tqdm

def splitByMonth(input_file, output_file):
    data_list = {}

    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)

        for row in csv_reader:
            month_data = row[11][:7]
            if month_data not in data_list:
                data_list[month_data] = []
            data_list[month_data].append(row)

    for month_data, rows in tqdm(data_list.items(), desc="处理进度", unit="文件"):
        file_path = os.path.join(output_file, f'{month_data}.csv')
        log_path = os.path.join(output_file, f'log.txt')

        with open(file_path, 'w', newline='', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(header)
            csv_writer.writerows(rows)

        with open(log_path, "a") as f:
            s = "{}\t{}\n".format(month_data, len(rows))
            f.write(s)
            f.close()

    print("文件划分完成！")
    
def main():
    csv_file_path = "data/sensor_positiondict_removed_5.csv"
    save_path = "data/split_month"

    os.makedirs(save_path, exist_ok=True)

    splitByMonth(csv_file_path, save_path)

# Call main()
if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))


