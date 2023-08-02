'''
@Coding : UTF-8
@File   : slide_window.py
@Time   : 2023-07-12 16:26:51
@Author : tanxh 
'''

import numpy as np
import pandas as pd

def sliding_window(data,window_size,step_size): # 往后找窗口
    for i in range(0,len(data) - window_size + 1,step_size):
        yield data[i:i + window_size]

def sliding_window1(data,window_size,step_size): # 往前找窗口
    for i in range(window_size,len(data) + 1,step_size):
        yield data[i - window_size:i]

def main(data,window_size,step_size):
    # 获取dataList结果
    window_generator = sliding_window(data,window_size,step_size)

    for window in window_generator:
        # return window
        print(window)

# Call main()
import time
if __name__ == "__main__":
    start_time = time.time()
    # main(['1','2','3','4','5','6','7','8','9','10'],5,1)

    start_date='20230131'
    end_date='20230630'
    date_2=pd.date_range(start=start_date, end=end_date, freq='S')
    print(date_2)

    '''
    DatetimeIndex(['2023-01-31 00:00:00', '2023-01-31 00:00:01',
               '2023-01-31 00:00:02', '2023-01-31 00:00:03',
               '2023-01-31 00:00:04', '2023-01-31 00:00:05',
               '2023-01-31 00:00:06', '2023-01-31 00:00:07',
               '2023-01-31 00:00:08', '2023-01-31 00:00:09',
               ...
               '2023-06-29 23:59:51', '2023-06-29 23:59:52',
               '2023-06-29 23:59:53', '2023-06-29 23:59:54',
               '2023-06-29 23:59:55', '2023-06-29 23:59:56',
               '2023-06-29 23:59:57', '2023-06-29 23:59:58',
               '2023-06-29 23:59:59', '2023-06-30 00:00:00'],
              dtype='datetime64[ns]', length=12960001, freq='S')
    '''

    # main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))



