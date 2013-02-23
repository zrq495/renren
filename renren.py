#!/usr/bin/env python
#coding=utf-8

'''
======================================
此程序根据 http://www.oschina.net/code/snippet_946076_17870
Adapted BY: zrq495
Mail:zrq495@gmail.com
======================================
'''
from sgmllib import SGMLParser
import sys,urllib2,urllib,cookielib
import datetime
import time
import sh
import os
import commands
import random
class spider(SGMLParser):
    def __init__(self,email,password):
        SGMLParser.__init__(self)
        self.h3=False
        self.h3_is_ready=False
        self.div=False
        self.h3_and_div=False
        self.a=False
        self.depth=0
        self.names=""
        self.dic={}   
         
        self.email=email
        self.password=password
        self.domain='renren.com'
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
        else:
            opener=urllib2.build_opener(cookieProc)
            urllib2.install_opener(opener)       

    def login(self):
        print '开始登录'
        url='http://www.renren.com/PLogin.do'
        postdata={
                  'email':self.email,
                  'password':self.password,
                  'domain':self.domain  
                  }
        req=urllib2.Request(
                            url,
                            urllib.urlencode(postdata)            
                            )
        
        self.file=urllib2.urlopen(req).read()
        idPos = self.file.index("'id':'")
        self.id=self.file[idPos+6:idPos+15]
        tokPos=self.file.index("get_check:'")
        self.tok=self.file[tokPos+11:tokPos+21]
        rtkPos=self.file.index("get_check_x:'")
        self.rtk=self.file[rtkPos+13:rtkPos+21]
    


    def publish(self,content):
        url1='http://shell.renren.com/'+self.id+'/status'
        postdata={
                  'content':content,
                  'hostid':self.id,
                  'requestToken':self.tok,
                  '_rtk':self.rtk,
                  'channel':'renren',
                  }
        req1=urllib2.Request(
                            url1,
                            urllib.urlencode(postdata)            
                            )
        self.file1=urllib2.urlopen(req1).read()
        print '%s:\n刚才使用你的人人账号 %s 发了一条状态\n内容为：(%s)'% (datetime.datetime.now(),self.email,postdata.get('content',''))



t = 0
#content=raw_input('请输入状态的内容：')
while True:
	time.sleep(t)
	#content = sh.fortune()
	content = os.popen('fortune').read()
	#a,content = commands.getstatusoutput('fortune')
	#content = commands.getoutput('fortune')
	#print content
	#print content
	content = '【有点儿意思】 ' + str(content)
	if len(content) > 240:
		continue;
	fp = open("/home/quan/time.txt", 'a+')
	fp.write(str(datetime.datetime.now()) + '	' + str(t) + '\n')
	fp.close()
	renrenspider=spider('your_email','password')
	renrenspider.login()
	renrenspider.publish(content)
	t = random.randint(2400, 4800)
