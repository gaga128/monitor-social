# -*- coding: utf-8 -*-
#****************************************************************
# 单线程
# Author     : HSN
# Version    : 1.0
# Date       : 2016-07-09
# Description:
#****************************************************************
import urllib,urllib2
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import socket

global urls
urls = ''

def runs(url):
    try:
        req = urllib2.Request(url)
        result = urllib2.urlopen(req,timeout=5).read().decode("UTF-8")
        return result
    except socket.timeout, e:
        print "timeout"
        sendEmail('Timeout Happened:'+url)
    except urllib2.HTTPError, e:
        print "timeout",e.code
    except urllib2.URLError, e:
        print "timeout"

def addURL(url):
    url ='\n'+url
    global urls
    urls += url
    return urls

def sendEmail(text):
    sender = 'bdtest@social-touch.com'
    receivers = ['lujia@social-touch.com','huangshengnan@social-touch.com']
    msg = MIMEText('There are Sth Wrong with URL:'+text,'plain','utf-8')
    msg['From'] = Header("测试sender",'utf-8')
    msg['To'] = Header("lujia,huangshengnan",'utf-8')
    msg['subject'] = Header("接口预警邮件",'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qiye.163.com',25)
        smtp.starttls()
        smtp.login('bdtest@social-touch.com','aa11!@#bb')
        smtp.sendmail(sender,receivers,msg.as_string())
        smtp.close()
        print "email sent"
    except smtplib.SMTPException:
        print "Error in sending"

def getAPI(urllist):
    try:
        for i in range(len(urllist)):
            result = runs(urllist[i])
            flag = json.loads(result)["flag"]
            desc = json.loads(result)["desc"]
            if flag==200:
                print urllist[i]
                #print 'Information:'+desc
                #print 'flag:',flag
                #print "working normally"
            else:
                if desc == u"执行失败":
                    print urllist[i]
                    print 'Information:',desc
                    print 'flag:',flag
                global urls
                urls = addURL(urllist[i])
        #print 'urls='+urls
        if urls == '':
            pass
        else:
            sendEmail(urls)
    except TypeError,e:
        print u"触发了TypeError：格式错误也许只是表象，表象下有可能有深层次的原因，比如超时"

#################################################
if __name__=='__main__':
    urllist = ['http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=searchTagRes&appkey=172139920&uid=oLceXjgDCcV-SR7TML1IegalxBss&startTime=0&endTime=1447776000&spread=true&tagIds=1,5,7'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansNumDistOfProperty&appkey=172140250&propertyName=life_cycle&startTime=1&endTime=1555555555'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansNumDistOfTagByCon&appkey=172139920&propertyName=life_cycle&propertyValue=&startTime=1&endTime=1555555555&parentClassId=1'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansListByFanPropertyAndTagCondi&appkey=172139920&page=1&pageSize=100&propertyName=life_cycle&propertyValue=import_period&classId=1'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansListByPropertiesAndTagId&appkey=172139920&tagId=11&page=1&pageSize=11&sortFlag=false&sortPropertyName=uid&sortType=asc&propertyCondition={"query_type":"or","queryconditionArr":[{"propertyname":"life_cycle","up_value":"1","down_value":"1"},{"propertyname":"life_cycle","up_value":"growth_period","down_value":"growth_period"}]}'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansListByFanPropertiesAndAppId&appkey=172139920&page=1&pageSize=11&sortFlag=false&sortPropertyName=uid&sortType=asc&propertyCondition={"query_type":"or","queryconditionArr":[{"propertyname":"life_cycle","up_value":"1","down_value":"1"},{"propertyname":"life_cycle","up_value":"Growing+Consumer","down_value":"Growing+Consumer"}]}'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansNumDistOfNatureProperty&appkey=172139920&groupFieldName=life_cycle&propertyCondition={"query_type":"or","queryconditionArr":[{"propertyname":"life_cycle","up_value":"Declined+Consumer","down_value":"Declined+Consumer"},{"propertyname":"life_cycle","up_value":"Growing+Consumer","down_value":"Growing+Consumer"}]}'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=searchForecastTagRes&appkey=172139920&uid=oLceXjqTHFg2Qju1FJqdxBWUYthA&startTime=0&endTime=1547776000'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansListByPropertiesAndClassId&appkey=172139920&classId=11&page=1&pageSize=11&sortFlag=false&sortPropertyName=uid&sortType=asc&propertyCondition={"query_type":"or","queryconditionArr":[{"propertyname":"life_cycle","up_value":"1","down_value":"1"},{"propertyname":"life_cycle","up_value":"growth_period","down_value":"growth_period"}]}'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getFansNumOfGroupFieldByPropertyCon&appkey=172140250&propertyName=life_cycle&startTime=1&endTime=1555555555&propertyValue=Mature+Consumer&statisPropertyName=active'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=444&passwd=746749378&method=getLatestTimeOfFansPropertyTagCount&appkey=172140250'\
                ,'http://api.data.social-touch.com:8091/cdapi/req?appid=11&passwd=918672562&appkey=172139920&tagIds=1,55&propertyCondition={"query_type":"and","queryconditionArr":[]}&page=1&pageSize=12&sortFlag=true&sortPropertyName=active_val&sortType=desc&method=getFansListByPropertiesAndTagIds']
    getAPI(urllist)
