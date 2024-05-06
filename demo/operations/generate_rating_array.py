import numpy as np
# 存储了评分生成函数


def generate_data(data_type, size):
    """
    生成指定评分风格和大小的评分数据。
    Parameters:
        data_type (int): 数据类型。0表示严苛型，1表示宽松型，2表示极端型，3表示中庸型。
        size (int): 生成数据的大小。
    Returns:
        numpy.ndarray: 生成的数据。
    """
    # 严苛型评分风格：
    if data_type == 0:
        a = 1 / 0.775
        b = 0.125 / (0.525 + 0.125) + 2
        data = np.random.normal(loc=b, scale=a, size=size)
        condition1 = data < 0
        data[condition1] = 1 + 1 / (1 - data[condition1])
        condition2 = (data >= 0) & (data < 0.5)
        data[condition2] = 4 + data[condition2] * 2
        condition3 = (data >= 0.5) & (data < 1)
        data[condition3] = (data[condition3] - 0.5) * 2
        condition4 = data > 5
        data[condition4] = 4 + 1 / (data[condition4] - 4)
    # 宽松型评分风格：
    elif data_type == 1:
        a = 1 / 0.95
        b = 0.265 / (0.265 + 0.685) + 3
        data = np.random.normal(loc=b, scale=a, size=size)
        condition1 = data < 1
        data[condition1] = 3 + 1 / (2 - data[condition1])
        condition2 = data > 5
        data[condition2] = 5 - 1 / (data[condition2] - 4)
    # 极端型评分风格：
    elif data_type == 2:
        a = 1 / 0.385
        b = 1
        data = np.random.normal(loc=b, scale=a, size=size)
        condition1 = data < -0.5
        data[condition1] = 3 + 2 / (0.5 - data[condition1])
        condition2 = (data >= -0.5) & (data < 1)
        data[condition2] = (data[condition2] + 0.5) * (2 / 3)
        condition3 = (data >= 2) & (data < 3)
        data[condition3] = 2 - 2 / (data[condition3] - 1)
        condition4 = data > 5
        data[condition4] = 5 - 1 / (data[condition4] - 4)
    # 中庸型评分风格：
    elif data_type == 3:
        a = 1 / 1.015
        b = 0.685 / (0.125 + 0.685) + 2 + 0.17
        data = np.random.normal(loc=b, scale=a, size=size)
        condition1 = data < 1
        data[condition1] = 3 + 2 / (2 - data[condition1])
        condition2 = data > 5
        data[condition2] = 5 - (data[condition2] - 4)
    else:
        raise ValueError("Invalid data type. Please choose between 0, 1, 2, or 3.")

    return data