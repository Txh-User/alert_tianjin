'''
@Coding : UTF-8
@File   : calculate_timegap.py
@Time   : 2023/07/08 18:50:45
@Author : tanxh 
'''

from dateutil.parser import parse
import time

def date_time_count_ms(startTime,endTime):
    a = parse(str(endTime))
    b = parse(str(startTime))
    
    d_count = (a - b).days  # 获取天数差
    s_count = (a - b).seconds  # 获取秒数差
    total_seconds = (a - b).total_seconds()  # 计算到毫秒

    hours, rem = divmod(total_seconds,3600) # divmod(x,y)，以元组形式返回x与y的商和余数
    minutes, seconds = divmod(rem,60)
    # print("ctime: {}, rectime: {}, 时间间隔为: {:0>2}:{:0>2}:{:0>6.3f}".format(startTime,endTime,int(hours),int(minutes),seconds))

    gaptime = "{:0>2}:{:0>2}:{:0>6.3f}".format(int(hours),int(minutes),seconds)

    # print(gaptime) 14:42:43.568
    return gaptime

def main(startTime,endTime):
    Duration = date_time_count_ms(startTime,endTime)
    return(Duration)

# Call main()
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("运行耗时：{:.4f}s".format(end_time - start_time))



