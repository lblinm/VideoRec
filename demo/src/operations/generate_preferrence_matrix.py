import csv
import numpy as np
import os


def createUserPreferenceMatrix(num_users, num_categories):
    """
    使用了隐式表示法，用户的uid由行数隐含
    偏好的值用大于1或者小于1的值表示，具体为多个分数转换成的小数
    :param num_users: 用户数
    :param num_categories: 视频类型(tags)数量
    :return: 在指定路径下的一个名为"user_preference_matrix.csv"的csv文件，其中包含随机生成的，用户对视频的偏好
    """
    # start_time = time.time()
    preference_slot = [1.2, 1.2, 1.1, 1.1, 1.1, 1, 1, 1, 1, 1, 0.9, 0.9, 0.8, 0.8]

    user_preference_csv = os.environ.get('DATA_PATH') + "\\user_preference_matrix.csv"
    with open(user_preference_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        column_headers = [f'Category_{i}' for i in range(num_categories)]
        writer.writerow(column_headers)
        for user_id in range(num_users):
            np.random.shuffle(preference_slot)
            writer.writerow(preference_slot)

    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"代码执行时间为: {execution_time} 秒")  #测试用
