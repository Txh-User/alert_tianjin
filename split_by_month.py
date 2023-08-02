'''
@Coding : UTF-8
@File   : split_by_month.py
@Time   : 2023/07/09 14:42:18
@Author : tanxh 
'''

import csv
import os
import time

def splitByMonth(csv_file_path, save_path, month):
    with open(csv_file_path, 'r', encoding='utf-8') as textfile:
        csvreader = csv.reader(textfile)
        header = next(csvreader)

        # save_path = save_path + "/{}".format(str(month))
        save_split_file = save_path + "/{}_{}".format('2023', month) + ".csv"
        print("保存路径：\t" + str(save_split_file))

        # 若路径不存在，创建
        if not os.path.exists(save_path):
            os.mkdir(save_path)
            print("创建文件夹：\t" + str(save_path))

        # 写入文件
        # f = csv.writer(open(save_split_file, "w", encoding="UTF-8", newline=""))
        f = csv.writer(open(save_split_file, "a", encoding="UTF-8", newline=""))
        f.writerow(header)
        
        linecnt = 0

        # 若月份相同，则写入当前行
        for row in list(csvreader):
            ctime = row[11]
            month_str = ctime[5:7]

            if(int(month_str) == month):
                f.writerow(row)
                linecnt += 1

    print("{} 已写入 {} 行".format(save_split_file, linecnt))

def main():
    csv_file_path = "data/sensor-alarm-info_final.csv"
    save_path = "data/split_month"


    if not os.path.exists(save_path):
        os.mkdir(save_path)
        print("创建文件夹：\t" + str(save_path))

    for month in range(1, 13):
        print("目标文件：\t" + str(csv_file_path))
        print("月份：\t" + str(month))

        splitByMonth(csv_file_path, save_path, month)

# Call main()
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))


