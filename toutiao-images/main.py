'''
@Author: 秋冬
@Date: 2020-04-24 17:28:43
'''
'''
我们要爬取今日头条的图片
步骤:
    根据分析,发现https://www.toutiao.com/search/?keyword=关键字 可以获得一个内容列表带有下面三种内容:
        1. 图片集
        2. 带图片的文章
        3. 视频
    我们只需要图片集和文章中的图片

    根据分析,我们发现内容列表是通过ajax获取内容的 https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E7%BE%8E%E5%A5%B3&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1587718768519&_signature=C8tUEAAgEBDgHSGri3a4TwvKFQAAFVvdfNDesF52EXhXbrDFVbozcvWYgwvlg3Ohy86IesJBKdYVIEUPadHhO37oJUCqQZheGic-p8WPmjfBXLfJgHx2mv6x-Dj33vFszCZ
    改变offset就可以请求新的内容列表
    
    ajax中,data字段就是正文内容,每条正文内容有三个控制属性:
    has_gallery 有没有图片集
    has_image 有没有图片
    has_video 有没有视频

    判断流程伪代码:
    if has_video:
        return
    if has_gallery:
        请求内容页面,因为图片集都在内容页面
    else 
        直接解析ajax中的image_list字段

    图集内容页分析:可以内容页图片的地址不是通过ajax请求,而是直接放在js的一个变量gallery中.
    我们对于图片集的获取就是通过正则提取内容

    我们对每一个图片封装成一个对象,包括 标题,图片地址,图片名称 三个字段,存入mongodb数据库
    并且把图片下载到本地    
'''
from urllib.parse import urlencode
import requests
from requests.exceptions import RequestException
import time

s=requests.session()
#获取内容列表
def getList(offset,keyword):
    # offset,keyword,timestamp,_signature
    data = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format':'json',
        'keyword':keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
        # ,'timestamp': timestamp,
        # '_signature': _signature
    }
    headers={
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    # url='https://www.toutiao.com/api/search/content/?' + urlencode(data)
    url=r'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E7%BE%8E%E5%A5%B3&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1587740449999&_signature=EMyYYAAgEBD7Gu3bBoKIiRDN2XAAE5zU0nDutOcI5RkR.pi0ctrv5gRtpdZq9fc4o8eZoO.RDQb0BH87WROPkmcBkLDrGMs2PtOEnzrxVKGKPvyHYkEy4v-djWilyE03Xc1'
    # res=s.get(url,headers=headers)
    res=requests.get(url,headers=headers)
    print(res.status_code)
    print(res.text)

def assembleData(offset,keyword):
     timestamp=getTimestamp()
     url='/api/search/content/'
     data = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format':'json',
        'keyword':keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': timestamp
    }

#获取时间戳(毫秒级)
def getTimestamp():
    timestamp=time.time()
    return int(round(timestamp*1000))

def getSignature(data):
    pass


def main():
    getList(0,'美女')
if __name__ == "__main__":
    main()
