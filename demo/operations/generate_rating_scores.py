import pandas as pd
import random
import math
import csv
from generate_rating_array import generate_data
from group_number_mapping import get_corresponding_video_groups
from generate_preferrence_matrix import createUserPreferenceMatrix
import time
import heapq

# 240430 20:02 02版本： 生成评分耗时538.56秒，三部分耗时：0，0.048，0.006
# 这个版本，假设了用户数，固定了视频的分组数量，并且假设了具体要看的视频个数
# 现在是03版本，以下是此版本拟优化or解决的问题
# 1.要求能够调整每个用户观看的视频数
#   1.1 根据拟观看视频数，计算出合适的min_rating_num，以及偏好评分观看的数量
# 2.尝试优化第二部分的时间复杂度
#   2.1 进行第二部分的时间复杂度分析
#   2.2 尝试优化时间复杂度，使其降低一个量级，其次再考虑常数级别的优化


def generate_rating(user_num, videos_watched_per_user):
    """
    目前函数会输出总用时，要删掉自行注释
    :param user_num: 用户数量
    :param videos_watched_per_user: 想要每个用户观看的视频数
    :return: 没有返回值，直接写入指定路径的csv文件
    """
    # 初始化偏好矩阵
    createUserPreferenceMatrix(user_num, 14)
    # 相关文件地址，请注意修改成本地文件地址
    csv_file = "rating.csv"
    preference_matrix = "user_preference_matrix.csv"
    tag_matrix = "E:\\DataStructure\\240428第二版本\\work_together-master\\source\\video_titles.csv"

    # 视频数量已定，假设用户数为10003，可以调整每个用户观看的视频数
    # user_num = 10003
    video_num = 118709
    # 用户组数也恒定为4，相关变量已经确定了
    user_per_group = math.floor(user_num / 4)
    user_remaining = user_num % 4  # 前user_remaining组实际数量是user_per_group+1

    # new: 确认用户数支持的最小视频组数，视频组数小生成速度理应更快
    minimal_unit = 12  # minimal_unit最视频组中每组的四分之一，初始为12
    for i in [44, 40, 36, 32, 28, 24, 20, 16, 12]:
        if video_num / i < user_per_group:
            minimal_unit = i / 4
            continue
        else:
            break

    # new:输入指定视频数量，计算出需要的min_rating_num与preferred_rating_num
    # videos_watched_per_user = 1000

    if videos_watched_per_user > 30 * minimal_unit:
        min_rating_num = math.floor(videos_watched_per_user / (6 * minimal_unit))
        preferred_rating_num = math.ceil(videos_watched_per_user / minimal_unit * (5/12))
    elif videos_watched_per_user < 15 * minimal_unit:
        min_rating_num = math.floor(videos_watched_per_user / (3 * minimal_unit))
        preferred_rating_num = math.ceil(videos_watched_per_user / minimal_unit / 3)
    else:
        min_rating_num = 5
        preferred_rating_num = math.ceil(videos_watched_per_user / (2 * minimal_unit) - 2.5)
    # print(f"目前的视频组最小单元{minimal_unit}均匀评分{min_rating_num}，实际{min_rating_num * minimal_unit};偏好评分{preferred_rating_num}，实际{preferred_rating_num *2 *minimal_unit}")

    # 第一步：对用户和视频分组 可以直接分块，也可以取余。这里直接取余

    # 暂定用户组数恒定为4，先确定视频组数
    video_group_num = 4 * minimal_unit

    # 这里取组数后是要保证除以组数后每组视频的个数比每组用户的个数小
    video_per_group = math.floor(video_num / video_group_num)
    video_remaining = video_num % video_group_num

    # 每组的个数要经常访问，用数组存储
    # 用户分组（取余法，不记录每组起始下标，只记录大小）
    user_groups = []
    # start_index = 0 # 若直接分块，要记录每块的起始索引
    for i in range(4):
        if i < user_remaining:
            group_size = user_per_group +1
        else:
            group_size = user_per_group
        user_groups.append(group_size)
    # 视频分组
    video_groups = []
    for i in range(video_group_num):
        if i < video_remaining:
            group_size = video_per_group + 1
        else:
            group_size = video_per_group
        video_groups.append(group_size)
    # 测试逻辑正确性，方便调试
    # print("用户分组情况:", user_groups)
    # print("视频分组情况:", video_groups)

    # 第二步：均匀打分：保证评分数量最低限
    # 可以用随机取替代直接对应关系，这里直接取余对应，余1->1,余0->4

    # 随机数生成也放入数组 以数组操作
    user_begin = []
    for i in range(4):
        temp = random.randint(0, user_groups[i])
        user_begin.append(temp)
    video_begin = []
    for i in range(video_group_num):
        temp = random.randint(0, video_groups[i])
        video_begin.append(temp)
    # print("用户分组初始随机数:", user_begin)
    # print("视频分组初始随机数:", video_begin)

    # 两个起始参数一出，每个用户要观看哪些视频已经确定了
    # 对应关系如下：offset = video_current - video_begin = user_current - user_begin
    # 访问时，永远访问 index = current % num ; 并连续访问 min_rating_num 次
    # video_current = (user_current - user_begin + video_begin + video_num_in_group) % video_num_in_group
    # 也就是说，只要输入两个begin随机值，就可以唯一确定指定用户要观看的视频
    # 但要注意：user_current - user_begin + video_begin > video_num_in_group + video_begin 时，对应的video_current实际不存在
    # 这个模型是存在组内小部分用户在均匀打分过程中所看视频不足video_num_in_group的，甚至没被分配到视频

    # 第三步：偏好评分
    # 假定：第a组均匀评分，则a+1、a+2两组对该组视频进行偏好打分
    # 要减小计算量，还是得二次减小区间，即仍然只取部分，累积覆盖完

    # 设置取视频的数量阈值
    min_preferred_rating_num = 100
    if preferred_rating_num * 5 > min_preferred_rating_num:
        min_preferred_rating_num = preferred_rating_num * 5
    # 先加上一个边界处理条件 # 逻辑如此，变量未更改，不可直接使用
    # if video_num_in_group < min_preferred_rating_num:
    #     min_preferred_rating_num = video_num_in_group



    # 初始化数据为数组的操作
    # 给定user_id，计算出其分组以及均匀评分分配到的视频
    start_time = time.time()

    data_preference = pd.read_csv(preference_matrix)
    data_tags = pd.read_csv(tag_matrix)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['uid', 'vid', 'rating'])

        for user_id in range(user_num):

            per_start_time = time.time()
            # 第一部分

            targeted_video = []  # 存储分配到的视频的容器
            user_group_index = user_id % 4
            uniform, preference = get_corresponding_video_groups(user_group_index, video_group_num)
            for video_index in uniform:
                current_user_id = user_id
                if user_id < user_begin[user_group_index]:
                    current_user_id += user_groups[user_group_index]
                if current_user_id - user_begin[user_group_index] + video_begin[video_index] < video_groups[video_index] + video_begin[video_index]:
                    for i in range(min_rating_num):
                        video_id = (current_user_id - user_begin[user_group_index] + video_begin[video_index] + i) % video_groups[video_index]
                        targeted_video.append(video_id * video_group_num + video_index)  # 载入的是视频的实际id，即还原取余操作后的id
            # print("id为", user_id, "的用户被分配到的视频id：", targeted_video)
            targeted_video_size = len(targeted_video)
            # print(targeted_video_size)

            per_end_time1 = time.time()
            # 第二部分

            for video_index in preference:
                current_user_id = user_id + video_begin[video_index]
                # video_stack = []
                # preference_stack = []

                # 启动最小堆存储，转换为TopK问题，需要取k为preferred_rating_num
                min_heap = []

                # 相比均匀评分，每个用户都要被分到一组视频
                for i in range(min_preferred_rating_num):
                    video_id = (current_user_id - user_begin[user_group_index] + video_groups[video_index] + i) % video_groups[video_index]
                    exact_video_id = video_id * video_group_num + video_index
                    # video_stack.append(exact_video_id) # 改成最小堆
                    temp_preference = data_preference.loc[user_id, f"Category_{data_tags.loc[exact_video_id, 'tag']}"]
                    if data_tags.loc[exact_video_id, 'play'] >= 10000:
                        temp_video_quality = 1.11
                    elif data_tags.loc[exact_video_id, 'play'] < 100:
                        temp_video_quality = 0.9
                    else:
                        temp_video_quality = 1

                    if len(min_heap) < preferred_rating_num:
                        heapq.heappush(min_heap, (temp_preference * temp_video_quality, exact_video_id))
                    else:
                        if temp_preference * temp_video_quality > min_heap[0][0]:
                            heapq.heappop(min_heap)
                            heapq.heappush(min_heap, (temp_preference * temp_video_quality, exact_video_id))
                    # preference_stack.append(temp_preference * temp_video_quality) # 改成最小堆
                # 对于每组，关于偏好进行排序

                # 以下部分改成最小堆
                # zip:python内置函数，用一个迭代器把数据打包成元组，若不等长截至短的耗尽
                # sorted:使用Timsort这种混合排序算法，结合了归并排序(Merge Sort)和插入排序(Insertion Sort)
                # sorted_stack = sorted(zip(preference_stack, video_stack), reverse=True)
                # for item in sorted_stack[:5]:
                #     targeted_video.append(item[1])

                # 最小堆方法
                for item in min_heap:
                    targeted_video.append(item[1])
            # print("id为", user_id, "的用户被分配到要进行选择性观看的视频id：", targeted_video)

            targeted_video_size = len(targeted_video)
            # print(targeted_video_size)
            rating = generate_data(user_id % 4, targeted_video_size)

            per_end_time2 = time.time()
            # 第三部分

            for i in range(targeted_video_size):
                temp_preference = data_preference.loc[user_id, f"Category_{data_tags.loc[targeted_video[i], 'tag']}"]
                if data_tags.loc[exact_video_id, 'play'] >= 200000:
                    temp_video_quality = 1.3
                elif data_tags.loc[exact_video_id, 'play'] >= 100000:
                    temp_video_quality = 1.25
                elif data_tags.loc[exact_video_id, 'play'] >= 10000:
                    temp_video_quality = 1.11
                elif data_tags.loc[exact_video_id, 'play'] >= 1000:
                    temp_video_quality = 1
                else:
                    temp_video_quality = 0.9
                writer.writerow([user_id, targeted_video[i], round(rating[i]*temp_preference*temp_video_quality if rating[i]*temp_preference*temp_video_quality <= 5 else 5, 3)])

            per_end_time3 = time.time()

            # 性能测试
            if user_id % 200 == 0:
                end_time2 = time.time()
                execution_time2 = end_time2-start_time
                print(f"目前处理到user_id:{user_id}到此消耗的时间为：{execution_time2}秒")
                print(f"第一部分耗时{per_end_time1-per_start_time}，第二部分耗时{per_end_time2-per_end_time1},第三部分耗时{per_end_time3-per_end_time2}")
                print(f"目标视频数量为{targeted_video_size}")

    end_time = time.time()

    execution_time = end_time - start_time
    print(f"用户评分消耗的时间为：{execution_time}秒")

