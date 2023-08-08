# [rawData]
包含 3687795 行数据<br>
sensor-alarm-info_sort.csv<br>
sensor-alarm-info_sort.json<br>
sensor-alarm-info.csv<br>
sensor-alarm-info.json<br>

# [codeFile]
1.计算同差值内的不同传感器发生频率的告警组（test1_count_sensor.py）

2.过滤错误的数据（test4_filter_wrongdata.py）

3.时间规整（time_warp.py）

4.按月分割告警数据（split_by_month.py）

5.按行分割告警数据（split_by_lines.py）

6.按列排序 csv 文件（sort_csv.py）

7.获取滑动窗口（slide_window.py）

8.消除抖动告警（aggregate_chatter_alarm.py）

9.计算告警状态（calculate_status.py）

10.计算告警时间间隔（calculate_timegap.py）

11.数据集的处理全过程，文件转换+过滤+排序+时间规整（dataset.py）

12.文件转换（json_to_csv.py）


# [processing]
1、json->csv，转换时间格式  "sensor-alarm-info_sort.json" -> "sensor-alarm-info_sort.csv"

2、过滤错误年份，写入正确数据，生成无误的数据集  "sensor-alarm-info_sort.csv" -> "sensor-alarm-info_filter.csv"

3、ctime-8h，计算timegap，加入表头  "sensor-alarm-info_filter.csv" -> "sensor-alarm-info_timewarp.csv"

4、按 ctime 排序  "sensor-alarm-info_timewarp.csv" -> "sensor-alarm-info_final.csv"


*使用滑动窗口收敛同窗口期内同位置传感器的 xx + dxx 组合拳*


# [pureData]
"sensor-alarm-info_filter.csv"<br>
除去原数据中的错误年份数据，累计去除 19038 行，剩余正确数据 3668757 行
<br>
nr + dnr：80740 行<br>
cr + dcr：37701 行<br>
nc + dnc：3550316 行<br>

"sensor-alarm-info_final.csv"<br>
处理完成的可用数据集

# [dataAggregation]
"sensor-alarm-info_remove_60.csv"<br>
对 sensor-alarm-info_final.csv 进行抖动告警收敛，窗口 60s，收敛后剩余 2167274 行，收敛率40.93%

"sensor-alarm-info_remove_300.csv"<br>
窗口 300s，收敛后剩余 2158651 行，收敛率41.16%

窗口大小对同文件的收敛率影响较小，收敛率受数据分布的影响较大

"sensor_positiondict_removed_5.csv"<br>
使用位置字典方法进行颤动告警收敛，截取时间为5min，剩余 263954 行，收敛率：92.81%

"sensor_positiondict_removed_10.csv"<br>
使用位置字典方法进行颤动告警收敛，截取时间为10min，剩余 199962 行，收敛率：94.55%

"sensor_windowlist_removed_5.csv"<br>
使用窗口列表截取方法进行颤动告警收敛，截取时间为5min，剩余 274357 行，收敛率：92.52%

"sensor_windowlist_removed_10.csv"<br>
使用窗口列表截取方法进行颤动告警收敛，截取时间为10min，剩余 208410 行，收敛率：94.32%

"sensor_group_5s.csv"<br>
找出告警发生间隔5s内的告警位置信息（用于后续apriori的关联挖掘）

"sensor_group_10s.csv"<br>
找出告警发生间隔10s内的告警位置信息




























