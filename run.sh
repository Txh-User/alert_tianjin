#!/bin/bash

# 设置运行次数和计时单位
n=10
time_unit="s"

total_time=0

# 循环运行python文件并累计运行时间
for ((i=1; i<=$n; i++)); do
    echo "Running iteration $i..."
    start_time=$(python -c 'import time; print(time.time())')  # 记录开始时间

    python -u aggregate_chatter_alarm.py  # 运行Python文件

    end_time=$(python -c 'import time; print(time.time())')  # 记录结束时间
    elapsed_time=$(echo "$end_time - $start_time" | bc)  # 计算运行时间

    total_time=$(echo "$total_time + $elapsed_time" | bc)  # 累计运行时间

    echo "Iteration $i completed in $elapsed_time seconds"
done

# 计算平均运行时间
average_time=$(echo "$total_time / $n" | bc)

# 输出平均运行时间
echo "Average running time: $average_time seconds"



