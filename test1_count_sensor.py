'''
@Coding : UTF-8
@File   : test1_count_sensor.py
@Time   : 2023-07-12 16:58:11
@Author : tanxh 
'''

import csv
from dateutil.parser import parse
from tqdm import tgrange

csv_file_path = "data/test/test_final.csv"
save_path = "data/test/test_final_group_5s.csv"
# csv_file_path = "data/sensor-alarm-info_final.csv"
# save_path = "data/sensor-alarm-info_final_group_5s.csv"

def date_time_count_ms(startTime,endTime): # 计算时间间隔
    a = parse(str(endTime))
    b = parse(str(startTime))

    d_count = (a - b).days  # 获取天数差
    s_count = (a - b).seconds  # 获取秒数差
    total_seconds = (a - b).total_seconds() # 计算到毫秒

    return total_seconds

def del_samesensor(List): # 列表去重
    new_sensorList = []
    for item in List:
        if item not in new_sensorList:
            new_sensorList.append(item)

    return new_sensorList

def calculate_list(List): # 列表计数（需要改进）
    counter_sdict = {}
    for item in List:
        counter_sdict[item] = counter_sdict.setdefault(item,0) + 1
    
    return counter_sdict

def write_header():
    # csv 文件表头
    headerList = ['group', 'count']

    # 创建 csv 文件，写入表头
    f = csv.writer(open(save_path,"w",encoding="UTF-8",newline=""))
    f.writerow(headerList)
    print("{} 表头写入完成".format(save_path))

def main():
    timeList = []
    sidList = []
    find_sidList = []
    new_sidList = []
    delta = 5.0 # 两条告警发生的间隔时间

    with open(csv_file_path,'r',encoding='utf-8') as textfile:
        print("读取文件：{}".format(csv_file_path))
        csvreader = csv.reader(textfile)
        header = next(csvreader)

        sidList_cnt = 0

        print("正在加载时间列表……")
        for row in list(csvreader):
            ctt = row[12]
            sid = row[0]
            
            timeList.append(ctt)
            sidList.append(sid)
        
        print("窗口大小：{}s".format(delta))
        print("正在计算告警组……")
        for i in range(1,csvreader.line_num - 1): # timeList[i]=sidList[i]

            # bname + lf


            if len(find_sidList) == 0:
                find_sidList.append(sidList[i-1])

            time_gap = date_time_count_ms(timeList[i - 1],timeList[i]) # 计算相邻两条告警发生的时间间隔
            is_sid_equal = sidList[i] != sidList[i - 1] # 两条告警的传感器不同

            # print("sid:{}, {}: {}, sid:{}, {}: {}".format(sidList[i],i - 1,timeList[i-1],sidList[i - 1],i,timeList[i]))
            # print("time_gap:{},{},sid_same:{}".format(time_gap,time_gap <= delta,sid_different))

            if time_gap <= delta: # 时间间隔小于时间窗口，表示两条告警在一个窗口内
                if is_sid_equal: # 发生告警的传感器不同
                    if sidList[i] not in find_sidList: # 当前窗口传感器计数内不存在该传感器
                        find_sidList.append(sidList[i])
                        # print(list(new_sidList))
                    else: # 当前窗口内已存在该传感器，不计
                        continue
                else: # 窗口内的重复传感器告警，可通过此再过滤等级
                    continue
            else: # 接连的两条告警不在时间窗口内，窗口计数list index+1
                new_sidList.append(find_sidList)
                find_sidList = []
                sidList_cnt += 1
    # print(new_sidList)

    alarmList = del_samesensor(new_sidList)
    print("告警组：{}".format(alarmList))
    # print("出现频次：{}".format(calculate_list(new_sidList)))

    write_header()

    print("正在写入：{}".format(save_path))
    for item in alarmList:
        # print(item) # ['Temp_3']
        f = csv.writer(open(save_path,"a",encoding="UTF-8"))
        f.writerow(item)

    print("写入完成：{}".format(save_path))

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))



