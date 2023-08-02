# -*- encoding: UTF-8 -*-
'''
@File        : aggregate_chatter_alarm.py
@Environment : 
@Description : 
@Time        : 2023-08-01 15:08:48
@Author      : tanxh 
'''

import os
import csv
from tqdm import tqdm
from dateutil.parser import parse
from datetime import datetime, timedelta

def status_judge(a, b):
    code = 0

    if(a[0] != 'd' and b[0] == 'd'): # i-1:dnc  i:nc
        code = 1
    elif(a[0] != 'd' and b[0] != 'd'): # i-1:nc  i:nc
        code = 2
    elif(a[0] == 'd' and b[0] != 'd'): # i-1:nc  i:dnc
        code = 3
    else: # i-1:dnc  i:dnc
        code = 4
    
    return code

def date_time_count_ms(start_time, end_time):
    a = parse(str(start_time))
    b = parse(str(end_time))

    total_second = (b - a).total_seconds

    return total_second

def find_data_in_window(input_file, output_file, window_size_minutes):
    rowList = [] # 记录所有行
    alarmList = [] # 记录需要保留的告警
    writeline = 0

    window_size = timedelta(seconds=window_size_minutes) # 窗口大小
    step_size = 1 # 步长

    with open(input_file,"r",encoding="UTF-8") as textfile:
        print("读取文件：{}".format(input_file))
        csvreader = csv.reader(textfile)
        header = next(csvreader)

        f = csv.writer(open(output_file, "w", encoding="UTF-8", newline=""))
        f.writerow(header)

        print("正在加载数据……")
        for row in tqdm(list(csvreader)): # 占内存……
            rowList.append(row)

        print("间隔时间：{}s".format(window_size))
        print("正在计算……")

        for i in tqdm(range(1, csvreader.line_num - 1)):
            alarm_now = rowList[i]
            alarm_previous = rowList[i - 1]

            # print("sid:{},bname:{},lf:{},status:{},ctime:{}".format(alarm_now[0], alarm_now[1], alarm_now[7], alarm_now[10], alarm_now[11]))

            time_gap = date_time_count_ms(alarm_previous[11], alarm_now[11]) # 计算相邻两条告警发生的时间间隔

            is_sid_same = (alarm_now[0] == alarm_previous[0]) # 传感器相同
            is_bname_same = (alarm_now[1] == alarm_previous[1]) # 板号相同
            is_lf_same = (alarm_now[7] == alarm_previous[7]) # 框相同

            is_all_same = (is_sid_same and is_bname_same and is_lf_same) # 位置都相同

            status_code = status_judge(alarm_now[10], alarm_previous[10]) # 获取当前与前一条告警之间的 status 关系

            if(time_gap <= window_size): # 
                if(is_all_same): # 当前与上一条告警处于同位置
                    if(status_code == 3): # i-1:nc  i:dnc
                        if(len(alarmList) == 0):
                            alarmList.append(alarm_previous)
                            alarmList.append(alarm_now)
                        else:
                            if(len(alarmList) > 1):
                                alarmList[1] = alarm_now
                            else:
                                alarmList.append(alarm_now)

                    elif(status_code == 2): # i-1:nc  i:nc
                        if(len(alarmList) == 0):
                            alarmList.append(alarm_previous)
                        else:
                            continue

                    elif(status_code == 1): # i-1:dnc  i:nc
                        if(len(alarmList) == 0):
                            alarmList.append(alarm_now)
                        else:
                            if(len(alarmList) > 1):
                                continue
                            else:
                                alarmList[0] = alarm_now
                                alarmList.append(alarm_previous)

                    elif(status_code == 4): # i-1:dnc  i:dnc
                        if(len(alarmList) > 1):
                            alarmList[1] = alarm_now
                        else:
                            alarmList.append(alarm_now)

                else:
                    for item in list(alarmList):
                        f = csv.writer(open(output_file, 'a', encoding='UTF-8', newline=""))
                        f.writerow(item)
                        writeline += 1
                    alarmList = []
                    alarmList.append(alarm_now)

            else:
                for item in list(alarmList):
                    f = csv.writer(open(output_file, 'a', encoding='UTF-8', newline=""))
                    f.writerow(item)
                    writeline += 1
                alarmList = []
                alarmList.append(alarm_now)


        print("{} 文件保存成功".format(output_file))
        print("剩余 {} 行，消除率：{:.2f}%".format(writeline, (1 - writeline / len(rowList)) * 100))

def find_matching_data_with_status(input_file, output_file, window_size_minutes):
    window_size = timedelta(minutes=window_size_minutes)
    result = []
    window_data = []
    print("窗口大小：{}".format(window_size))

    with open(input_file, 'r', newline='') as csvfile:
        print("读取文件：{}".format(input_file))

        reader = csv.reader(csvfile)
        fieldnames = next(reader)  # 读取表头
        datalen = 0
        prev_position = None
        prev_window_end = None

        print("正在计算……")
        for row in tqdm(list(reader)):
            datalen += 1
            timestamp = datetime.strptime(row[11], '%Y-%m-%d %H:%M:%S')

            if not prev_window_end:
                # 初始化第一个窗口
                prev_window_end = timestamp + window_size

            if timestamp > prev_window_end:
                # 当前数据时间戳超出窗口，处理前置窗口数据并重置窗口
                process_window_data(window_data, result)
                window_data = []
                prev_window_end = timestamp + window_size

            # 保存当前行的位置信息
            position = (row[0], row[1], row[7])

            if position == prev_position:
                # 将位置相同的数据添加进窗口
                window_data.append(row)
            else:
                # 当位置不相同时，处理前置窗口数据并更新位置
                process_window_data(window_data, result)
                window_data = [row]
                prev_position = position

        # 处理最后一个窗口数据
        process_window_data(window_data, result)

        print("原有 {} 行，剩余 {} 行，收敛率：{:.2f}%".format(datalen, len(result), (1 - len(result) / datalen) * 100))

    # 写入文件
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(result)

    print("{} 文件保存成功".format(output_file))

def process_window_data(window_data, result):
    if not window_data:
        return

    # 在窗口数据中找到所有的 sid、bname、lf
    positions = set((item[0], item[1], item[7])for item in window_data)

    for position in positions:
        # 筛选出当前位置的所有数据
        position_data = [item for item in window_data if (item[0], item[1], item[7]) == position]
        # 筛选出当前位置的状态
        status_values = set(item[10] for item in position_data)

        # 判断当前位置的所有状态，找出第一条 nc 与最后一条 dnc，添加进 result
        if ('nc' or 'nr' or 'cr') in status_values and ('dnc' or 'dnr' or 'dcr') in status_values:
            first_faulty_data = next(item for item in position_data if item[10][0] != 'd')
            last_normal_data = next(item for item in reversed(position_data) if item[10][0] == 'd')

            result.append(first_faulty_data)
            result.append(last_normal_data)

def find_matching_data_with_status1(input_file, output_file, window_size_minutes):
    window_size = timedelta(minutes=window_size_minutes)
    result = []
    print("窗口大小：{}".format(window_size))

    with open(input_file, 'r', newline='') as csvfile:
        print("读取文件：{}".format(input_file))
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        prev_window_end = None
        positions_data = {}
        datalen = 0

        print("正在计算…")
        for row in tqdm(list(reader)):
            datalen += 1
            timestamp = datetime.strptime(row['ctime'], '%Y-%m-%d %H:%M:%S')

            if not prev_window_end:
                # 初始化第一个窗口
                prev_window_end = timestamp + window_size

            if timestamp > prev_window_end:
                # 当前数据时间戳超出窗口，处理前置窗口数据并重置窗口
                process_window_data1(positions_data, result)
                positions_data = {}
                prev_window_end = timestamp + window_size

            # 将当前行的位置信息保存为一个元组，并将数据添加到对应位置的列表中
            position = (row['sid'], row['bname'], row['lf'])

            if position not in positions_data:
                positions_data[position] = []

            positions_data[position].append(row)

        # 处理最后一个窗口数据
        process_window_data1(positions_data, result)

        print("原有 {} 行，剩余 {} 行，收敛率：{:.2f}%".format(datalen, len(result), (1 - len(result) / datalen) * 100))

    # 写入文件
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result)

    print("{} 文件保存成功".format(output_file))

def process_window_data1(positions_data, result):
    for data in positions_data.items():
        status_values = set(item['status'] for item in data)

        if 'nc' in status_values and 'dnc' in status_values:
            first_faulty_data = next(item for item in data if item['status'] == 'nc')
            last_normal_data = next(item for item in reversed(data) if item['status'] == 'dnc')

            result.append(first_faulty_data)
            result.append(last_normal_data)

def main():
    # 窗口大小，单位：min
    window_size_minutes = 10

    # 文件路径
    csv_file_path = "data/status/status_nc.csv"
    save_path = "data/status/nc_removed_{}min1.csv".format(window_size_minutes)
    # csv_file_path = "data/sensor-alarm-info_final.csv"
    # save_path = "data/sensor_removed_{}.csv".format(window_size_minutes)
    
    # find_data_in_window(csv_file_path, save_path, window_size_minutes)

    # solution 1
    # find_matching_data_with_status(csv_file_path, save_path, window_size_minutes)

    # solution 2
    find_matching_data_with_status1(csv_file_path, save_path, window_size_minutes)


# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))


