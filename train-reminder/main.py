# -*- coding: utf-8 -*-

import requests
import re
import time

'''
关闭HTTPS证书验证警告

有可能会报No module named requests.packages.urllib3,那是因为requests版本低,没有urllib3模块
使用下面命令安装2.6.0版本就解决了
pip install --upgrade --force-reinstall 'requests==2.6.0' urllib3 
'''
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}


'''
使用server酱推送消息
title 消息标题
info 消息内容
'''
def send_msg(title,info):
    url=('https://sc.ftqq.com/SCU92306T720aa3d22514912ba47be0fd854826ef5e85b1970ff90.send?'
        'text={}&desp={}').format(title,info)
    requests.get(url)
'''
 获取城市站点和代码对应规则
'''
def get_city_station_code():
    url="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9142"

    r = requests.get(url,verify=False,headers=headers)
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = re.findall(pattern,r.text)
    city_station_rule=dict(result)
    return city_station_rule

'''
# 拼接我们的请求URL
from_station_name 起始站名
to_station_name 终点站名
date 出发日期(格式:yyyy-MM-dd)
ticket_type 票类型(ADULT或0X00)
'''
def get_query_url(from_station_name,to_station_name,date,ticket_type="ADULT"):
    station_rule=get_city_station_code()
    from_station_code=station_rule[from_station_name]
    to_station_code=station_rule[to_station_name]
    url=('https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes={}'
    ).format(date,from_station_code,to_station_code,ticket_type)
    return url

'''
请求获取结果,并解析出我们想要的数据,用server酱推送
'''
def query_analysis_send(url):
    #需要先获取cookie,才能得到想要的数据
    s=requests.session()
    r= s.get('https://kyfw.12306.cn/otn/leftTicket/init',headers=headers)
    r= s.get(url,verify=False,headers=headers)
    raw_trains=r.json()['data']['result']
   
    train_info='' #最后发送的信息
    info_list=[]
    for raw_train in  raw_trains:
        data_list = raw_train.split('|')
        #车次
        train_no=data_list[3]
        #出发时间
        start_time = data_list[8]
        #到达时间
        arrive_time = data_list[9]
        #二等座票数(如果没有会是空,所以弄个'--'占位符)
        second_seat=data_list[30] or '--'
        #打印结果
        info = ('车次:{} ,'
            '出发时间:{} ,'
            '到达时间:{} ,'
            '二等座票数:{}\n'
        ).format(train_no,start_time,arrive_time,second_seat)
        #print(info)
        if(second_seat.isdigit()):
            info_list.append(info)
    #把info_list通过server酱推送到微信,这里面包含了我们需要的信息,并且返回Ture
    if(info_list.__len__()>0):
        for value in info_list:
            train_info+=value+'\n'
        send_msg(title='有票啦',info = train_info)
        return True

if __name__ == "__main__":
    #拼接url
    url = get_query_url("南昌","上海","2020-04-17")
    # 死循环,等待query_analysis_send结束循环
    while True:
        time.sleep(1) 
        #请求结果,解析数据并推送
        if query_analysis_send(url):
            break

