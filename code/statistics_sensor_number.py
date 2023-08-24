# -*- encoding: UTF-8 -*-
'''
@File        : statistics_sensor_number.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-17 13:41:30
@Author      : tanxh 
'''

import csv
from tqdm import tqdm
from datetime import datetime, timedelta

def status_jduge(a:str):
    if(a[0] == 'd'):
        return 1
    elif(a == 'nc'):
        return 2
    elif(a == 'cr'):
        return 3
    elif(a == 'nr'):
        return 4
    
def findNumberOfSensor(input_file, output_file, window_size_minutes):
    result = {}
    
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

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

    res = {}

    for key, data in tqdm(result_dict.items(), desc="遍历数据行"): # 遍历每行
        window_start = datetime.strptime("00:00:00", "%H:%M:%S")
        window_end = window_start + timedelta(minutes=window_size_minutes)

        status_count = 0
        data_index = 0

        while data_index < len(data): # 在行中滑窗口，每个窗口遍历一次行数据，找到在当前窗口内的数据
            time_str, status = data[data_index]
        
            time_obj = datetime.strptime(time_str, "%H:%M:%S").time()

            # 当前时间不在窗口内，则一直滑动窗口，添加状态值
            while (not (window_start.time() < time_obj <= window_end.time())):
                if str(window_start.time()) == '23:55:00' and str(window_end.time()) == '00:00:00':
                    break
               
                if key not in res:
                    res[key] = []
                res[key].append(status_count)

                window_start = window_end
                window_end = window_end + timedelta(minutes=window_size_minutes)

            # 当前时间在窗口内，则开始记录状态数量
            if status == 1:
                status_count -= 1
            else:
                status_count += 1

            data_index += 1

        # 处理最后一个窗口
        while len(res.get(key, [])) < 288:
            res.setdefault(key, []).append(status_count)
            
    with open(output_file, "w") as f:
        for position, rows in tqdm(res.items(), desc="写入文件"):
            s = '{}\t\t{}\t\t{}\t\t{}\n'.format(position[2], position[1], position[0], rows)
            f.write(s)

    print("写入完成！")

def main():
    window_size = 5

    csv_file_path = "./data/split_day_before/2023-05-15.csv"
    savepath = "./log/sensor_number.txt"

    findNumberOfSensor(csv_file_path, savepath, window_size)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("运行耗时：{:.4f}s".format(end_time - start_time))

