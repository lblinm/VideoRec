import requests
import re
import time
import csv
import random

#====================爬取某视频网站的视频标题===================
#使用注意：
#1. 把headers里的cookie、user-agent改为自己电脑浏览该网页的值
#2. 修改csv_file_path为想要存储爬取结果的路径
#===========================================================

headers = {
    'cookie': 'BIDUPSID=23BC72449B7C422320D0B0E11776CDF6; PSTM=1688092726; BAIDUID=23BC72449B7C422320D0B0E11776CDF6:SL=0:NR=10:FG=1; BAIDUID_BFESS=23BC72449B7C422320D0B0E11776CDF6:SL=0:NR=10:FG=1; BAIDU_WISE_UID=wapp_1688092760731_667; BDUSS=EEtRHBHN0d-RzlYMU5LMEp4cFB4d3ZvNy1tRGwzdTJpb01QajdOMmMzaW5maWhtRVFBQUFBJCQAAAAAAAAAAAEAAAC139D4Ymxpbm1sb29uAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKfxAGan8QBme; BDUSS_BFESS=EEtRHBHN0d-RzlYMU5LMEp4cFB4d3ZvNy1tRGwzdTJpb01QajdOMmMzaW5maWhtRVFBQUFBJCQAAAAAAAAAAAEAAAC139D4Ymxpbm1sb29uAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKfxAGan8QBme; ZFY=VxicPkqID1zY3NlPZsAf:BkN9475x3bFCmEaQRyrUT0M:C; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1710813995,1712627269; ZD_ENTRY=bing; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1712644276; ariaDefaultTheme=undefined; RT="z=1&dm=baidu.com&si=c81d71ac-eeeb-4048-9810-ab3cd3f37170&ss=lurq2r18&sl=j&tt=qec&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=a3y8u&ul=a4efw&hd=a4f0s"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
}

csv_file_path = 'E:/project/rec/videos.csv' #视频标题写入此

def random_sleep(mu=0.7, sigma=0.3):
    '''正态分布随机睡眠
    :param mu: 平均值
    :param sigma: 标准差，决定波动范围
    '''
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)


videos = []
#爬取好看视频网页的视频标题，21个标签，每个标签30次，每次20条，共21*30*20=12600条(实际12567条)
url = 'https://haokan.baidu.com/haokan/ui-web/video/rec' 
#21个视频标签
tags = ['yingshi_new','yinyue_new','youxi_new','gaoxiao_new','zongyi_new',
        'yule_new','dongman_new','shenghuo_new','guangchuangwu_new','meishi_new',
        'chongwu_new','sannong_new','junshi_new','shehui_new','tiyu_new','keji_new',
        'shishang_new','qiche_new','qinzi_new','wenhua_new','lvyou_new']


for tag_index in range(0,21):
    for scraw_index in range(0,30):
        timestamp = int(time.time())
        now_time = timestamp*10000
        params = {
            'tab': tags[tag_index],
            'act': 'pcFeed',
            'pd': 'pc',
            'num': '20',
            'shuaxin_id': str(now_time),
            'hk_timestamp': str(now_time),
        }
        response = requests.get(url=url, params=params, headers=headers)
        html_data = response.json()
        videos_info = html_data['data']['response']['videos']
        for i in videos_info:
            videos.append(i['title'])
        print(f"tag:{tag_index+1}/21  scraw:{scraw_index+1}/30")
        random_sleep()
    
with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['vid', 'title'])
    for index, item in enumerate(videos):
        writer.writerow([index, item])