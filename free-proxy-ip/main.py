#python免费代理ip,我们以西刺代理为例
import requests
from pyquery import PyQuery as pq
import subprocess as sp
import re
'''
原理分析:
1. 通过爬虫爬取西刺网站的免费代理,封装到一个列表中,字段取`协议`,`ip`,`端口`
2. 通过subproccess调用系统ping命令来验证ip有效性.无效的就剔除掉,无效ip有两种可能:
    1. 存在该ip但是链接不上,可以找到丢包和延迟的信息
    2. 不存在该ip,找不到丢包和延迟的信息
'''
#提取网页的`协议`,`ip`,`端口`
def xiciParser(html):
    proxyList=[]
    doc=pq(html)
    itemsIter=doc('#ip_list tr').items()
    for tr in itemsIter:
        ip=tr('td:nth-child(2)').text()
        port=tr('td:nth-child(3)').text()
        protocol=tr('td:nth-child(6)').text()
        proxyList.append((protocol,ip,port))
    return proxyList[1:]

#获取代理ip列表
def getProxyList(page):
    #席次代理的ip页面规则是http://www.xicidaili.com/nn/页码
    xici_url='http://www.xicidaili.com/nn/%s' %(page)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    s=requests.session()
    res=s.get(url=xici_url,headers=headers)
    html=''
    if res.status_code==200:
        res.encoding='utf-8'
        html=res.text
    return xiciParser(html)

#检测ip的有效性,最终返回延迟时间
'''
正在 Ping 127.0.0.1 具有 32 字节的数据:
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128
来自 127.0.0.1 的回复: 字节=32 时间<1ms TTL=128

127.0.0.1 的 Ping 统计信息:
    数据包: 已发送 = 3，已接收 = 3，丢失 = 0 (0% 丢失)，
往返行程的估计时间(以毫秒为单位):
    最短 = 0ms，最长 = 0ms，平均 = 0ms
'''
def checkIP(ip):
    # -n 3代表发送三次请求,-w 3代表最长等待时间3秒
    cmd ="ping -n 3 -w 3 %s" %(ip)
    #stdout=sp.PIPE表示,执行后的输出结果赋值给stdout变量,我们通过分析stdout就可以知道请求的结果
    p=sp.Popen(cmd,stdout=sp.PIPE,shell=True)
    #cmd命令默认输出字符编码是'gbk'
    out=p.stdout.read().decode('gbk')
    #开始分析结果
    #匹配丢包数的正则
    lostPacketRe=re.compile(u'丢失 = (\d+)')
    waitTimeRe=re.compile(u'平均 = (\d+)ms')
    lostPacket=lostPacketRe.findall(out)
    #如果匹配规则lostPacket失效,那么代表ip根本不存在,认为三次都丢包
    if len(lostPacket) == 0:
        lose=3
    else:
        lose = int(lostPacket[0])
    #如果丢包超过两个就默认延迟1000毫秒
    if lose >2:
        return 1000
    #如果丢包数小于等于2,就判断延迟时间
    else:
        waitTime=waitTimeRe.findall(out)
        #如果找不到延迟的时间,也是找不到ip,所以返回延迟1000
        if len(waitTime)==0:
            return 1000
        else:
            return int(waitTime[0])

#对代理ip列表进行测试,延迟200毫秒以内的都保留,最终返回有效ip列表
#就算是有效ip,但是也要注意,这种烂大街的ip,可能会被一些网站封锁
def proxyListfilter(proxyList):
    length=len(proxyList[0:20])
    i=0
    for proxy in proxyList[0:20]:
        protocol,ip,port=proxy
        waitTime=checkIP(ip)
        if waitTime>200:
            proxyList.remove(proxy)
            i+=1
            print(ip+'是无效的ip,无效个数 '+str(i)+' / '+str(length))
    return proxyList
        
        





if __name__ == "__main__":
    proxyList=getProxyList(1)
    proxyListfilter(proxyList)
    


