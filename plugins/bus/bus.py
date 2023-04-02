# encoding:utf-8

from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
import plugins
from plugins import *
from common.log import logger
from bs4 import BeautifulSoup
import requests

UM_BUS_LOOP = 'https://campusloop.cmdo.um.edu.mo/zh_TW/busstopinfo'

@plugins.register(name="BusReminder", desc="A simple plugin that give you the UM campus Bus imformation.", version="0.1", author="Minami", desire_priority= 100)
class BusReminder(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[BusReminder] inited")
        
    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
        content = e_context['context'].content[:]
        clist = e_context['context'].content.split(maxsplit=1)
        if clist[0] == "$巴士":
            response = requests.get(UM_BUS_LOOP)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            spans = soup.find_all('span')
            for span in spans:
                print(span.text)
            reply = Reply()
            reply.type = ReplyType.TEXT
            busString1, busString2 = self.getcontent()
            msg = e_context['context']['msg']
            if e_context['context']['isgroup']:
                reply.content = "我无法在群聊中提供巴士报站服务"
            else:
                reply.content = busString1 + " " + busString2
            e_context['reply'] = reply
            e_context.action = EventAction.BREAK_PASS # 事件结束，并跳过处理context的默认逻辑
    
    def getcontent(self):
        # 发送HTTP请求并获取HTML响应
        response = requests.get(UM_BUS_LOOP)
        html = response.content
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')
        # 获取所有<span>标签的内容
        spans = soup.find_all('span')
        divs = soup.find_all('div', {'class': 'main'})
        busActivate=False
        busNumber=0
        busInfoLength=3
        busInfo=[]
        StateInfo=[]
        busStop=[]
        returnString1=""
        returnString2=""
        if len(spans)>=12:
            busActivate=True
            busInfoLength=4
        for i in range(busInfoLength):
            busInfo.append(spans[i].prettify().replace('<span>','').replace('</span>','').replace('\n','').replace(' ',''))
        for div in divs:
            right_divs = div.find_all('div', {'class': 'right'})
            right_divs1 = div.find_all('div', {'class': 'out-right'})
            if right_divs:
                right=right_divs[0]
            else:
                right=right_divs1[0]
            #left_divs = divs.find_all('div', {'class': 'left'})
            left_divs = div.find_all('div', {'class': 'left'})
            left_divs1 = div.find_all('div', {'class': 'left out-left'})
            if left_divs:
                left=left_divs[0]
            else:
                left=left_divs1[0]
            if left.text.strip() == '':
                busStop.append([right.prettify().replace('<span>','').replace('</span>','').replace('\n','').replace(' ','').replace('<divclass="right">','').replace('</div>','').replace('<divclass="out-right">',''),0])
            else:
                busNumber += 1
                busStop.append([right.prettify().replace('<span>','').replace('</span>','').replace('\n','').replace(' ','').replace('<divclass="right">','').replace('</div>','').replace('<divclass="out-right">',''),1])
        if busActivate==False:
            returnString1="当前暂无巴士服务"
        else:
            if busNumber==0:
                    returnString1="当前暂无巴士"
                    returnString2=busInfo[1]
            else:
                for busPosition in busStop:
                    if busPosition[1] == 1:
                        returnString1 = busPosition[0]
        return returnString1, returnString2