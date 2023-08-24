'''
@Coding : UTF-8
@File   : json_to_csv.py
@Time   : 2023-07-14 16:33:43
@Author : tanxh 
'''

import csv
import json
import time
import calculate_timegap

# Parameters
# json_file = "data/test/test.json"
# csv_file_path = "data/test/test.csv"
json_file = "data/sensor-alarm-info_sort.json"
csv_file_path = "data/sensor-alarm-info_sort.csv"

dataList = []

def read_json():
    print("读取文件：{}".format(json_file))
    read_cnt = 1
    # 读取 json 文件，将数据读入 dataList 缓存
    with open(json_file,"r",encoding="UTF-8") as F:
        for line in F:
            dataDict = json.loads(line)
            dataList.append(dataDict)
            print("已读取 {} 行".format(read_cnt))
            read_cnt += 1
            
    print("{} 读取完成".format(json_file))

def write_header():
    # csv 文件表头
    headerList = ['sid', 'bname', 'bip', 'uip', 'lr', 'ln',
                'lc', 'lf', 'sval', 'alevel', 'status', 
                'ctime', 'ctt', '@timestamp', 'rectime',#'gaptime',
                'ecode', 'recstat', 'etype', '@version',]

    # 创建 csv 文件，写入表头
    f = csv.writer(open(csv_file_path,"w",encoding="UTF-8",newline=""))
    f.writerow(headerList)
    print("{} 表头写入完成".format(csv_file_path))

def write_csv():
    # 将 dataList 中的数据写入 csv 文件
    write_cnt = 1
    for item_name in dataList:
        print("正在写入: {}/{}".format(write_cnt,len(dataList)))
        f = csv.writer(open(csv_file_path,"a",encoding="UTF-8",newline=""))

        # 时间格式变换 2023-06-06T09:18:42Z -> 2023-06-06 09:18:42
        ctime = item_name['ctime']
        ctime_str = ctime[0:10] + ' ' + ctime[11:19]

        ctt = item_name["ctt"]
        ctt_str = ctt[0:10] + ' ' + ctt[11:23]

        timestamp = item_name["@timestamp"]
        timestamp_str = timestamp[0:10] + ' ' + timestamp[11:23]

        rectime = item_name["rectime"]
        rectime_str = rectime[0:10] + ' ' + rectime[11:23]

        # gaptime = calculate_timegap.main(ctime_str,rectime_str)
        # print("1-{},2-{},gap:{}".format(ctime_str,rectime_str,gaptime))
        
        f.writerow([item_name["sid"], item_name["bname"], item_name["bip"], item_name["uip"], item_name["lr"], item_name["ln"],
                    item_name["lc"], item_name["lf"], item_name["sval"], item_name["alevel"], item_name["status"], 
                    ctime_str, ctt_str, timestamp_str, rectime_str, #gaptime,
                    item_name["ecode"], item_name["recstat"], item_name["etype"], item_name["@version"]])
        write_cnt += 1
        
    print("{} 写入完成".format(csv_file_path))

def main():
    read_json()
    write_header()
    write_csv()

    # return csv_file_path

# Call main()
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))



