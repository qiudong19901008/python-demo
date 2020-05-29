from pyquery import PyQuery as pq
import requests
from csv import DictWriter
import csv
import re
import time
import json


'''
步骤:
    1.分析页面,抓取必要的信息(城市名-小区名)
    2.通过百度地图api把地点转化为经纬度.
    3.使用百度地图提供的html页面根据经纬度热度列表绘制热力图    
'''
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}

#根据城市和小区名,获取地理坐标
def getLocation(city,livingArea):
    bdurl='http://api.map.baidu.com/geocoding/v3/?address='
    output='json'
    ak='yFNSVYweL3GHyTUP7nEVxxZtG1oIQoCr'
    callback='showLocation'
    uri=bdurl+livingArea+'&output='+output+'&ak='+ak+'&callback='+callback+'&city='+city
    res=requests.get(uri)
    #提取经度与维度
    lng=re.findall(r'lng":(\d+\.?\d+)',res.text)[0]
    lat=re.findall(r'lat":(\d+\.?\d+)',res.text)[0]
    return lng+','+lat

#获取链家网站所有城市和代码的对应关系
def getCityCodeList():
    url='https://www.lianjia.com/city/'
    res=requests.get(url,headers=header)
    doc=pq(res.text)
    pattern=re.compile(r'<a\shref=["|\'].*//(\w{2}).*">(.*)<')
    cityCodeList={}
    aList=doc('.city_list_ul a').items()
    for a in aList:
        matcher=pattern.match(str(a))
        cityCodeList[(matcher.group(2))]=matcher.group(1)
    return cityCodeList
    
#每个元组的格式(小区地址,热度,房屋样式(几室几厅),房屋大小,房价)
#text 需要解析的html页面
def parseHouseInfo(text):
    houseInfoList=[]
    doc=pq(text)
    infoList=doc('.sellListContent li').items()
    for info in infoList:
        #小区名地址address
        subAddress=[i.text() for i in info('.positionInfo').items('a')]
        address=subAddress[1]+subAddress[0]
        #热度hot
        hot=re.findall(r'^(\d+)人',info('.followInfo').text())[0]
        #样式style,面积space
        (style,space,abandon)=re.findall(r'(\d{1}室\d{1}厅).*\s(\d+(\.\d+)?平米)',info('.houseInfo').text())[0]
        #价格price
        price=info('.totalPrice span').text()+'万'
        houseInfoList.append((address,hot,style,space,price))
    return houseInfoList

#根据城市名,获取指定页数的房屋信息,写入文件,默认100页
def crawlToFile(city,pg=100):
    houseFile = open(city+'.csv','w',newline='')
    houseHeader=['address','location','hot','style','space','price']
    csvWriter=DictWriter(houseFile,houseHeader)
    csvWriter.writeheader()
    cityCodeList=getCityCodeList()
    cityCode=cityCodeList[city]
    baseUrl='https://'+cityCode+'.lianjia.com/ershoufang/pg'
    for i in range(1,pg+1):
        res=requests.get(baseUrl+str(i),headers=header)
        time.sleep(1)
        # (小区地址,热度,房屋样式(几室几厅),房屋大小,房价)
        houseInfoList=parseHouseInfo(res.text)
        for houseInfo in houseInfoList:
            address,hot,style,space,price = houseInfo
            location=getLocation(city,address)
            houseRow={
                'address':address,
                'location':location,
                'hot':hot,
                'style':style,
                'space':space,
                'price':price
            }
            csvWriter.writerow(houseRow)
    houseFile.close()

#通过二手房的csv文件,获取需要的数据(经度,维度,热度)
#经纬度放在第二列,由逗号分割.热度放在第六列
def getHotMapData(filepath):
    hotMapData=[]
    with open(filepath) as houseInfo:
        reader=csv.reader(houseInfo)
        for row in reader:
            lngAndLat=row[1].split(',')
            if len(lngAndLat)==2:
                lng=float(lngAndLat[0])
                lat=float(lngAndLat[1])
                hot=int(re.findall(r'\d+',row[5])[0])
                subData={'lng':lng,'lat':lat,'count':hot}
                hotMapData.append(subData)
    #把热力图数据写入json文件备用
    hotMapJson=json.dumps(hotMapData)
    with open('hotMap.json','w') as hotMapFile:
        hotMapFile.write("var points="+hotMapJson)

#下一步就是复制http://lbsyun.baidu.com/jsdemo.htm#c1_15的html文件,准备绘制热力图
#这个html是百度给我们的,我们只要给它数据,修修改改就能变成热力图了











#测试
if __name__ == "__main__":
    # location=getLocation('沈阳','中海康城橙郡')
    # getCityCodeList()
    # crawlToFile('沈阳')
    # getHotMapData('沈阳.csv')

    #把指定城市数据爬取到一个csv文件
    # crawlToFile('沈阳')
    #把该csv文件数据提取到json文件
    getHotMapData('沈阳.csv')

