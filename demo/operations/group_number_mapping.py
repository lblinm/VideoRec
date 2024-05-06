def get_corresponding_video_groups(user_group_num,video_group_num):
    video_groups_first = []
    video_groups_second = []

    # 计算第一个组号集：视频组号 % 4 = 用户组号 n
    for i in range(video_group_num):  # 假设有12个视频组
        if i % 4 == user_group_num:
            video_groups_first.append(i)

    # 计算第二个组号集：(视频组号 + 1) % 4 = 用户组号 n 或 (视频组号 + 2) % 4 = 用户组号 n
    for i in range(video_group_num):  # 假设有12个视频组
        if (i + 1) % 4 == user_group_num or (i + 2) % 4 == user_group_num:
            video_groups_second.append(i)

    return video_groups_first, video_groups_second