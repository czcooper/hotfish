# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import urllib2,urllib

URL='http://ucenter.dadeinvest.com/membership-login/'
default_timeout=12

def get_login_status():
    base_web=urllib2.urlopen(URL,timeout=default_timeout).read()
    print base_web
    return base_web
    

if __name__ == "__main__":
    get_login_status()