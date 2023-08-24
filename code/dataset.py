'''
@Coding : UTF-8
@File   : dataset.py
@Time   : 2023-07-19 15:45:44
@Author : tanxh 
'''

from tqdm import tgrange
from dateutil.parser import parse
import json_to_csv,test4_filter_wrongdata,sort_csv,time_warp

json_file = ""

def main():
    json_to_csv_file = json_to_csv.main(json_file) # json 文件转 csv
    csv_filter_file = test4_filter_wrongdata.main(json_to_csv_file) # csv 文件过滤错误数据
    csv_sort_file = sort_csv.main(csv_filter_file) # csv 文件按时间排序
    csv_warp_file = time_warp(csv_sort_file) # csv 文件时间规整
    print("文件{}处理完毕".format(csv_warp_file)) # 处理完毕

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))

    