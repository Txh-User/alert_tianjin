'''
@Coding : UTF-8
@File   : split_by_lines.py
@Time   : 2023/07/10 10:45:31
@Author : tanxh 
'''

from pathlib import Path
import pandas as pd

# csv_file_path = Path("data/test.csv")
csv_file_path = Path("data/sensor-alarm-info_sort.csv")
split_size = 950000 # 子文件行数
save_path = csv_file_path.parent / ("split_lines") # 保存路径

if not save_path.exists():
    save_path.mkdir()
    print("创建文件夹：\t" + str(save_path))

print("保存路径：\t" + str(save_path))
print("目标文件：\t" + str(csv_file_path))
print("分割大小：\t" + "{:,}".format(split_size))

tmp = pd.read_csv(csv_file_path,nrows = 10)
columns = tmp.columns.to_list() # 获取表头

idx = 0
while(len(tmp) > 0):
    start = 1 + (idx * split_size)
    tmp = pd.read_csv(csv_file_path,header=None,names=columns,skiprows=start,nrows=split_size)
    if len(tmp) <= 0:
        break

    file_name = save_path.name + "_{}-{}".format(start, start + len(tmp))+".csv"
    file_path = save_path / file_name
    tmp.to_csv(file_path, index=False)
    idx += 1
    
    print(file_name + "\t保存成功")
 

 