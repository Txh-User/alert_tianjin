# -*- encoding: UTF-8 -*-
'''
@File        : statistics_sensor_per_bname.py
@Environment : TJalarm
@Description : 
@Time        : 2023-08-15 16:17:04
@Author      : tanxh 
'''

import csv
import os
from dateutil.parser import parse
from tqdm import tqdm
from datetime import timedelta

def date_time_count_ms(startTime, endTime): # 计算时间间隔
    a = parse(str(endTime))
    b = parse(str(startTime))

    d_count = (a - b).days  # 获取天数差
    s_count = (a - b).seconds  # 获取秒数差
    total_seconds = (a - b).total_seconds() # 计算到毫秒

    return total_seconds

def del_samesensor(List):
    unique_tuples = set()
    new_sensorList = []
    for item in List:
        # 元组转换为可哈希的类型，例如字符串或者元组中不可变的部分
        hashable_item = tuple(item)  # 假设元组中不可哈希的部分在元组内是不可变的
        if hashable_item not in unique_tuples:
            unique_tuples.add(hashable_item)
            new_sensorList.append(item)
    return new_sensorList

def count_sensor(input_file, output_file, delta):
    window_size = timedelta(minutes=delta)
    timeList = []
    sidList = []
    bnameList = []
    find_sidList = []
    new_sidList = []

    with open(input_file, 'r', encoding='UTF-8') as csvfile:
        print("正在处理文件：{}".format(input_file))
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        
        print("正在加载数据列表")
        for row in list(csvreader):
            ctt = row[12]
            sid = row[0]
            bname = row[1]
            
            timeList.append(ctt)
            sidList.append(sid)
            bnameList.append(bname)
        
    print("窗口大小：{}".format(window_size))
    print("正在计算告警组")

    # timeList[i]=sidList[i]
    for i in range(1, csvreader.line_num - 1):

        if len(find_sidList) == 0:
            # find_sidList.append((sidList[i - 1], bnameList[i - 1]))
            find_sidList.append(sidList[i - 1])

        # 计算相邻两条告警发生的时间间隔
        time_gap = date_time_count_ms(timeList[i - 1], timeList[i])

        # print("time_gap:{},{},sid_same:{}".format(time_gap,time_gap <= delta,sid_different))

        # 时间间隔小于
        if time_gap <= delta:
            # 发生告警的位置不同
            if sidList[i] != sidList[i - 1]:
                # position = (sidList[i], bnameList[i])
                position = sidList[i]
                # 当前窗口计数内不存在该位置
                if sidList[i] not in find_sidList:
                    
                    find_sidList.append(position)
                else: # 当前窗口内已存在该位置，不计
                    continue
            else: # 窗口内的重复位置告警
                continue
        else: 
            # 接连的两条告警不在时间窗口内
            new_sidList.append(find_sidList)
            find_sidList = []

    print("正在去重")
    alarmList = del_samesensor(new_sidList)
    # print("出现频次：{}".format(calculate_list(new_sidList)))

    # 写入文件
    print("正在写入：{}".format(output_file))
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(alarmList)

    print("写入完成")

def main():
    # 两条告警发生的间隔时间
    delta = 30.0

    save_path = "data/sensor_group_{}min_1.csv".format(int(delta))

    base_directory = "data/split_bname"

    # 遍历第一层子目录
    for dir_level1 in os.listdir(base_directory):
        dir_level1_path = os.path.join(base_directory, dir_level1)
        if os.path.isdir(dir_level1_path):
            # 遍历第二层子目录
            for dir_level2 in os.listdir(dir_level1_path):
                dir_level2_path = os.path.join(dir_level1_path, dir_level2)
                if os.path.isdir(dir_level2_path):
                    # 遍历第三层子目录
                    for dir_level3 in os.listdir(dir_level2_path):
                        dir_level3_path = os.path.join(dir_level2_path, dir_level3)

                        # dir_level3_path = 'data/split_bname/R0-P06/R0-P06D/NRM02.csv'
                        count_sensor(dir_level3_path, save_path, delta)

    # 写入文件

# Call main()
import time
if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    print("运行耗时：{:.4f}s".format(end_time - start_time))


