# -*- encoding: UTF-8 -*-
'''
@File        : test1_count_sensor.py
@Environment : TJalarm
@Description : findind the sensors that alarm together
@Time        : 2023-08-07 15:03:08
@Author      : tanxh 
'''

import csv
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
    for item in tqdm(List):
        # 元组转换为可哈希的类型，例如字符串或者元组中不可变的部分
        hashable_item = tuple(item)  # 假设元组中不可哈希的部分在元组内是不可变的
        if hashable_item not in unique_tuples:
            unique_tuples.add(hashable_item)
            new_sensorList.append(item)
    return new_sensorList


def count_sensor(input_file, output_file, delta):
    window_size = timedelta(minutes=delta)
    timeList = []
    positionList = []
    find_positionList = []
    new_positionList = []

    with open(input_file, 'r', encoding='UTF-8') as csvfile:
        print("读取文件：{}".format(input_file))
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        
        print("正在加载数据列表")
        for row in list(csvreader):
            ctt = row[12]
            position = (row[0], row[1], row[7])
            
            timeList.append(ctt)
            positionList.append(position)
        
        print("窗口大小：{}".format(window_size))
        print("正在计算告警组")

        # timeList[i]=positionList[i]
        for i in tqdm(range(1, csvreader.line_num - 1)):

            if len(find_positionList) == 0:
                find_positionList.append(positionList[i - 1])

            # 计算相邻两条告警发生的时间间隔
            time_gap = date_time_count_ms(timeList[i - 1], timeList[i])

            # 两条告警的发生位置不同
            is_position_equal = positionList[i] != positionList[i - 1]

            # print("time_gap:{},{},position_same:{}".format(time_gap,time_gap <= delta,position_different))

            # 时间间隔小于
            if time_gap <= delta:
                
                # 发生告警的位置不同
                if is_position_equal:

                    # 当前窗口计数内不存在该位置
                    if positionList[i] not in find_positionList:
                        find_positionList.append(positionList[i])
                        # print(list(new_positionList))

                    else: # 当前窗口内已存在该位置，不计
                        continue
                else: # 窗口内的重复位置告警
                    continue
            else: 
                # 接连的两条告警不在时间窗口内
                new_positionList.append(find_positionList)
                find_positionList = []

    print("正在去重")
    alarmList = del_samesensor(new_positionList)
    # print("出现频次：{}".format(calculate_list(new_positionList)))

    # 写入文件
    print("正在写入：{}".format(output_file))
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(alarmList)

    print("写入完成")

def main():
    # 两条告警发生的间隔时间
    delta = 5.0 

    # csv_file_path = "data/test/test_final.csv"
    # save_path = "data/test/test_final_group_5s.csv"
    csv_file_path = "data/sensor-alarm-info_final.csv"
    save_path = "data/sensor_group_{}s.csv".format(int(delta))

    count_sensor(csv_file_path, save_path, delta)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))



