'''
@Coding : UTF-8
@File   : test4_filter_wrongdata.py
@Time   : 2023/07/07 16:29:55
@Author : tanxh 
'''

import csv
import time

def calculate_list(List): # 列表计数
    counter_sdict = {}
    for item in List:
        counter_sdict[item] = counter_sdict.setdefault(item, 0) + 1
    
    return counter_sdict

def calculate_wrong_data():
    csv_file_path = "data/sensor-alarm-info_sort.csv"
    save_path = "data/sensor-alarm-info_filter.csv"
    # csv_file_path = "data/test/test.csv"
    # save_path = "data/test/test_filter.csv"

    year_list = []
    sid_list = []
    right_cnt = 0
    file_line = 0
    with open(csv_file_path, 'r', encoding='UTF-8') as csvfile:
        print("读取文件：{}".format(csv_file_path))
        csvreader = csv.reader(csvfile)
        header = next(csvreader) # 获取表头

        f = csv.writer(open(save_path, "w", encoding="UTF-8", newline="")) #打开文件写入表头
        f.writerow(header)

        for row in list(csvreader):
            file_line += 1
            col_data = row[11] # ctime
            if(col_data[0:4] != '2023'): # 若年份不为2023，则记录下发生次数
                print("找到 {} 行错误, ctime: {}, sid: {}".format(len(year_list) + 1, col_data[:10], row[0]))
                year_list.append(col_data[0:4])
                sid_list.append(row[0])
            else: # 若年份为2023，则将该行写入新文件
                right_cnt += 1
                # print("正在写入：{}".format(save_path))
                f = csv.writer(open(save_path, "a", encoding="UTF-8", newline=""))
                f.writerow(row)
                
        
    print("统计完毕，共找到 {} 行错误数据，错误率：{:.2f}%".format(len(year_list), (len(year_list) / file_line) * 100))
    print("错误数据总计:\nyear: {}\nsensor: {}".format(calculate_list(year_list), calculate_list(sid_list)))
    print("{} 保存成功，共写入 {} 行".format(save_path, right_cnt))
    
def main():
    calculate_wrong_data()

# Call main()
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))




    