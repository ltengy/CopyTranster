# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 08:24:48 2018

@author: ltengy
"""
import urllib #http连接需要用到
import json  #解析网页数据用
import win32clipboard as wc #读取剪切板数据
from pymouse import PyMouse #获得当前鼠标信息
import Tkinter         #自带的GUI库，生成文本框
import time          #定时器，减少占用
import win32con
currentData=''  

def transMousePosition():
    m = PyMouse()
    return "300x50+"+str(m.position()[0]-300)+"+"+str(m.position()[1]-15)
#获得剪切板数据	
def getCopyText():
    try:
        wc.OpenClipboard()
        copy_text = wc.GetClipboardData(win32con.CF_TEXT)
        copy_text=copy_text.strip().replace("\r\n"," ").replace("\n"," ").replace("\r"," ")
    except TypeError: 
        copy_text= "the text or failed to read text not found"
    finally :
        wc.CloseClipboard()
    return copy_text
#返会是否有新的复制数据
def newCopyData():
    if cmp(currentData,str(getCopyText()))!=0:
        return 1
    else: 
        return 0
#得到所有翻译文本
def getTransText(jsonText):
    text=''
    for listValue in jsonText['translateResult'][0]:
            text+= listValue['tgt']
    return text
  
if __name__ == '__main__':
    req_url = 'http://fanyi.youdao.com/translate'  # 创建连接接口，这里是有道词典的借口
    # 创建要提交的数据
    currentData=str(getCopyText())
    Form_Date = {}
    Form_Date['doctype'] = 'json'
    
       # main loop
    while True:
        if newCopyData():
            currentData=str(getCopyText())#取得当前剪切板数据
            Form_Date['i'] = currentData # 传递数据
            data = urllib.urlencode(Form_Date).encode('utf-8') #数据转换
            response = urllib.urlopen(req_url, data) #提交数据并解析
            html = response.read().decode('utf-8')  #服务器返回结果读取
            translate_results = getTransText(json.loads(html))  #以json格式载入
            position=transMousePosition()#取得当前鼠标位置
            top = Tkinter.Tk()#窗口初始化
            top.wm_attributes('-topmost',1)#置顶窗口
            top.geometry(position)#指定定位生成指定大小窗口
            e=Tkinter.Text()#生成文本框部件
            e.insert(1.0,translate_results)#插入数据
            e.pack()#将部件打包进窗口
            top.mainloop()# 进入消息循环
        currentData=str(getCopyText())
        time.sleep(1)
        
    