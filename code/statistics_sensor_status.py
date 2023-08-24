# -*- encoding: UTF-8 -*-
'''
@File        : statistics_sensor_status.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-16 14:49:53
@Author      : tanxh 
'''

import csv
from tqdm import tqdm

def status_jduge(a:str):
    if(a[0] == 'd'):
        return 1
    elif(a == 'nc'):
        return 2
    elif(a == 'cr'):
        return 3
    elif(a == 'nr'):
        return 4

def findFrequencyOfSensor(input_file, output_file):
    result = {}
    
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for row in tqdm(list(reader), desc="数据添加"):
            lf = row[7]
            bname = row[1]
            sid = row[0]
            ctime = row[11][11:]
            status = row[10]

            positions = (sid, bname, lf)

            if positions not in result:
                result[positions] = []

            result[positions].append((ctime, status_jduge(status)))

    # 对结果字典中的第三项（lf）进行排序
    sorted_data = sorted(result.items(), key=lambda item: item[0][2])

    result_dict = dict(sorted_data)

    with open(output_file, "w") as f:
        for position, rows in tqdm(result_dict.items(), desc="计算状态"):
            s = "{}\t\t{}\t\t{}\t\t{}\n".format(position[2], position[1], position[0], rows)
            f.write(s)
    
    print("写入完成！")

def main():
    csv_file_path = "./data/split_day_before/2023-05-15.csv"
    savepath = "./log/sensor_status_05-15.txt"

    findFrequencyOfSensor(csv_file_path, savepath)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("运行耗时：{:.4f}s".format(end_time - start_time))

