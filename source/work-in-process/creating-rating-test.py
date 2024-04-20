import numpy as np


# 定义函数用于计算概率分布
def calculate_distribution(data):
    # 计算直方图
    # bins 参数接受的是一个包含了区间划分点的列表，这些划分点可以是整数也可以是浮点数。
    hist, bins = np.histogram(data, bins=[-np.inf, 0, 1, 2, 3, 4, 5, np.inf])
    # 计算每个区间的概率
    probabilities = hist / len(data) * 100  # 将概率转换为百分比
    # 规范化概率总和为100%
    probabilities /= np.sum(probabilities) / 100
    return probabilities


# 第一组数据
a1 = 1 / 0.775
b1 = 0.125 / (0.525 + 0.125) + 2
data1 = np.random.normal(loc=b1, scale=a1, size=10000)
# 条件一：s < 0
condition1 = data1 < 0
data1[condition1] = 1 + 1 / (1 - data1[condition1])
# 条件二：0 <= s < 0.5
condition2 = (data1 >= 0) & (data1 < 0.5)
data1[condition2] = 4 + data1[condition2] * 2
# 条件三：0.5 <= s < 1
condition3 = (data1 >= 0.5) & (data1 < 1)
data1[condition3] = (data1[condition3] - 0.5) * 2
# 条件四：s > 5
condition4 = data1 > 5
data1[condition4] = 4 + 1 / (data1[condition4] - 4)


# 第二组数据
a2 = 1 / 0.95
b2 = 0.265 / (0.265 + 0.685) + 3
data2 = np.random.normal(loc=b2, scale=a2, size=10000)
# 条件一：s < 1 [3,4)
condition1 = data2 < 1
data2[condition1] = 3 + 1 / (2 - data2[condition1])
# 条件二：s > 5 [4,5]
condition2 = data2 > 5
data2[condition2] = 5 - 1 / (data2[condition2] - 4)

# 第三组数据
a3 = 1 / 0.385
b3 = 1
data3 = np.random.normal(loc=b3, scale=a3, size=10000)
# 条件一：s < -0.5
condition1 = data3 < -0.5
data3[condition1] = 3 + 2 / (0.5 - data3[condition1])
# 条件二：-0.5 <= s < 1
condition2 = (data3 >= -0.5) & (data3 < 1)
data3[condition2] = (data3[condition2] + 0.5) * (2/3)
# 条件三：2 <= s < 3
condition3 = (data3 >= 2) & (data3 < 3)
data3[condition3] = 2 - 2 / (data3[condition3] - 1)
# 补充条件： [3,3.5)->[3,4)  [3.5,4)->[4,5] 可调整[3,4)与[4,5]的比例，但另要两个调整，消耗大
# 条件四：s > 5
condition4 = data3 > 5
data3[condition4] = 5 - 1 / (data3[condition4] - 4)

# 第四组数据
a4 = 1 / 1.015
b4 = 0.685 / (0.125 + 0.685) + 2 + 0.17
data4 = np.random.normal(loc=b4, scale=a4, size=10000)
# 条件一：s < 1
condition1 = data4 < 1
data4[condition1] = 3 + 2 / (2 - data4[condition1])
# 条件二：s > 5
condition2 = data4 > 5
data4[condition2] = 5 - (data4[condition2] - 4)

print("第一组数据在不同区间的分布概率（百分比）：")
for i, prob in enumerate(calculate_distribution(data1)):
    print(f"区间{i}: {prob:.2f}%")

print("\n*************************\n")

print("第二组数据在不同区间的分布概率（百分比）：")
for i, prob in enumerate(calculate_distribution(data2)):
    print(f"区间{i}: {prob:.2f}%")

print("\n*************************\n")

print("第三组数据在不同区间的分布概率（百分比）：")
for i, prob in enumerate(calculate_distribution(data3)):
    print(f"区间{i}: {prob:.2f}%")

print("\n*************************\n")

print("第四组数据在不同区间的分布概率（百分比）：")
for i, prob in enumerate(calculate_distribution(data4)):
    print(f"区间{i}: {prob:.2f}%")
