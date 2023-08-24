'''
@Coding : UTF-8
@File   : sort_csv.py
@Time   : 2023-07-14 09:33:54
@Author : tanxh 
'''

import pandas as pd

# csv_file_path = "data/test/test_filter.csv"
# csv_save_path = "data/test/test_filter_sort.csv"
csv_file_path = "data/sensor-alarm-info_filter.csv"
csv_save_path = "data/sensor-alarm-info_filter_sort.csv"

def main():
    print("正在读取文件{}".format(csv_file_path))
    dataFrame = pd.read_csv(csv_file_path)

    print("正在排序……")
    dataFrame.sort_values("ctime", axis=0, ascending=True,inplace=True, na_position='first')

    dataFrame.to_csv(csv_save_path,index=False)
    print("文件{}排序成功".format(csv_save_path))

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))

