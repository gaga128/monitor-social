# -*- coding: utf-8 -*-
#****************************************************************
# 单线程
# Author     : lujia
# Version    : 1.0
# Date       : 2016-07-09
# Description:
#****************************************************************
import urllib,urllib2
import json
import requests
import xlrd
import os
import threading
import socket
import smtplib
from email.mime.text import MIMEText
from email.header import Header
global urls
urls = ''



def getAPI(interpath):
    try:
        data=xlrd.open_workbook(interpath)
        table=data.sheet_by_name('interface')
        nrows=table.nrows
        global name
        for i in range(1,nrows):
            name=table.cell(i,0).value
            method=table.cell(i,1).value
            httpstr=table.cell(i,2).value
            para=eval(table.cell(i,3).value )    ##将字符串转化为字典      eval()将字符串str当成有效的表达式来求值并返回计算结果。
            runs(method,httpstr,para)
        if urls == '':
            pass
            print 'Monitor pass!'
        else:
            print urls
            sendEmail(urls)
    except TypeError,e:
        print "TypeError： please check to see if there are any problems, such as timeout"
        sendEmail('TypeError： please check to see if there are any problems, such as timeout')


def runs(method,httpstr,para):
    try:
        if method == 'POST':
            req = requests.post(url=httpstr,data=para,timeout=7)
            url=httpstr + str(para)
        elif method == 'GET':
            req = requests.get(url=httpstr,params=para,timeout=7)
            url=req.url
        result=req.text
        # print '\ninterface name:%s,url:%s,\nresult:%s' % (name, url, result)
        if 'code' in json.loads(result):
            # ident = json.loads(result)['code']
            # info = json.loads(result)['msg']
            pass
        elif 'flag' in json.loads(result):
            # ident = json.loads(result)['flag']
            # info = json.loads(result)['desc']
            pass
        else:
            # ident = '0000000'
            # info = u'失败'
            print '\ninterface name:%s,url:%s,result:%s'%(name,url, result)
            global urls
            urls = addURL(url)
        # if ident == 200 or ident==20200:
        #     pass
        # # elif info != u'成功' or info != u'执行成功':
        # else:
        #     global urls
        #     urls = addURL(url)
        return result
    except requests.Timeout, e:
        print "The request timed out"
        sendEmail('The request timed out:name:%s method:%s %s %s' % (name,method,httpstr,para))
    except socket.timeout, e:
        print "timeout"
        sendEmail('The request timed out:name:%s method:%s %s %s' % (name, method, httpstr, para))
    except requests.ConnectionError, e:
        print  'ConectionError--please check your network connection!'
    except requests.HTTPError, e:
        print "HTTPError-timeout",e.code
    except urllib2.URLError, e:
        print "URLError-timeout"




def addURL(httpurl):
    httpurl ='\n'+httpurl
    global urls
    urls += httpurl
    return urls



def sendEmail(text):
    sender = 'bdtest@social-touch.com'
    receivers = ['lujia@social-touch.com']
    msg = MIMEText('There are Sth Wrong with URL:' + text, 'plain', 'utf-8')
    msg['From'] = Header("测试sender", 'utf-8')
    msg['To'] = Header("lujia,huangshengnan", 'utf-8')
    msg['subject'] = Header("接口预警邮件", 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qiye.163.com', 25)
        smtp.starttls()
        smtp.login('bdtest@social-touch.com', 'bbaa11!!')
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.close()
        print "email sent"
    except smtplib.SMTPException:
        print "Error in sending"


#################################################
if __name__=='__main__':
    getAPI(os.getcwd()+'/SCRM-interface_20170110.xlsx')
