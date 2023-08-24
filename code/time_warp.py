'''
@Coding : UTF-8
@File   : time_warp.py
@Time   : 2023-07-14 11:16:57
@Author : tanxh 
'''

import csv
from datetime import timedelta
from dateutil.parser import parse
import calculate_timegap

# csv_file_path = "data/sensor-alarm-info_filter_sort.csv"
# save_path = "data/sensor-alarm-info_final.csv"
csv_file_path = "data/test/test_filter_sort.csv"
save_path = "data/test/test_final.csv"

def write_header():
    # csv 文件表头
    headerList = ['sid', 'bname', 'bip', 'uip', 'lr', 'ln',
                'lc', 'lf', 'sval', 'alevel', 'status', 
                'ctime', 'ctt', '@timestamp', 'rectime',#'gaptime',
                'ecode', 'recstat', 'etype', '@version',]

    # 创建 csv 文件，写入表头
    f = csv.writer(open(save_path, "w", encoding="UTF-8", newline=""))
    f.writerow(headerList)
    print("{} 表头写入完成".format(save_path))

def write_csv():
    # 将 dataList 中的数据写入 csv 文件
    write_cnt = 1
    with open(csv_file_path, "r", encoding="UTF-8") as csvfile:
        print("读取文件：{}".format(csv_file_path))
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        print("正在写入: {}".format(save_path))
        for row in csvreader:
            ctime = row[11]
            rectime = row[14]

            # ctime 往前移8h
            new_ctime = parse(str(ctime)) - timedelta(hours=8)
            # print(new_ctime)

            f = csv.writer(open(save_path, "a", encoding="UTF-8", newline=""))

            gaptime = calculate_timegap.main(new_ctime,rectime)
            # print("1-{},2-{},gap:{}".format(new_ctime,rectime,gaptime))
            
            f.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], 
                        new_ctime, row[12], row[13], row[14], #gaptime, 
                        row[15], row[16], row[17], row[18]])
            write_cnt += 1
        
    print("写入完成：{}".format(save_path))

def main():
    write_header()
    write_csv()

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))


