# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,sys,thread
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import web
import time
#import model
#import MySQLdb
import hashlib
#from omp_maxpain import maxpain,get_all_opurl,get_all_crash_value
from free_db import free_list,free_symb_list
from login_status import get_login_status
from debug import logprint
from omp_maxpain import mp_index_page

#reload(sys) 
#sys.setdefaultencoding('utf8')
#sys.path.append("./buffettfaq")
#import faqmodel

LOGIN_URL="http://ucenter.dadeinvest.com/membership-login/"
LOGOUT_URL="http://ucenter.dadeinvest.com/membership-login/?swpm-logout=true"

web.config.debug = True 

urls = (
    '/', 'Index',
    '/index','Index',
    '/login','Login',
    '/logout','Logout',
    '/signup','Signup',
    '/testonly','Testonly',
    '/maxpain','MaxPain',
    '/omp','OptionsMaxPain',
    '/free','Free',
    '/pricing','Price',
    '/route','Route',
    '/whatismaxpain','WhatisMaxPain',
    )



app_root = os.path.dirname(__file__)
#db=model.db
#webdb=model.webdb
#URL开始



#from bae.core.wsgi import WSGIApplication
#application = WSGIApplication(app.wsgifunc())

def logged():
    if session.login==1:
        return True
    else:
        return False
    
class Testonly:

    def GET(self):
        """ Show page """
        teststr=str(session.login)
        return render.test(teststr)

    
def create_render(privilege):
    if logged():
        if privilege == 0:#游客
            render = web.template.render('templates/', base='base',globals=t_globals)
        elif privilege == 1:#普通用户
            render = web.template.render('templates/', base='base',globals=t_globals)
        elif privilege == 2:#后台管理
            render = web.template.render('templates/admin', globals=t_globals)
        else:
            render = web.template.render('templates/', base='base',globals=t_globals)
    else:
        #未登录用户
        render = web.template.render('templates/', base='base',globals=t_globals)
    
    return render

class Login:

    def GET(self):
        """
        if logged():
            render = create_render(session.privilege)
            return '%s' % render.login_double()
        else:
        """  
        referer = web.ctx.env.get('HTTP_REFERER', LOGIN_URL)
        if referer in [LOGIN_URL,LOGOUT_URL]:
            #清除上一次的session
            #session.kill()
            session.login = 1
            session.privilege = 1
            #return render.test(referer)
            render = create_render(session.privilege)
            return '%s' %render.login_success()
        else:
            #如果来源不对则返回登录页面
            raise web.seeother(referer)
    
class Logout:

    def GET(self):
        session.login = 0
        session.privilege = 0
        #session.kill()
        render = create_render(session.privilege)
        #session清零后，调用Ucenter接口真正退出
        raise web.seeother(LOGOUT_URL)
    
class Index:

    def GET(self):
        """ Show page """
        render = create_render(session.privilege)
        try:
            return render.index()
            #return "test OK le"
        except Exception,e:
            return logprint(str(e))

def get_max_crash_value(cvlists):
    max_temp=0
    
    for cv in cvlists:
        if cv['callvalue']>=cv['putvalue']:
                    max_temp=cv['callvalue']
        else:
                    max_temp=cv['putvalue']
                    
    return max_temp
        
def get_omp_page(render,symb,expdate):
    ompinfo=mp_index_page(symb,expdate)
    mp=ompinfo[0]
    call_chains=ompinfo[1]
    put_chains=ompinfo[2]
    cv_lists=ompinfo[3]
    opurls_tuple=ompinfo[4]
    current_expdate=ompinfo[5]
    short_name=ompinfo[6]
    maxcv=get_max_crash_value(cv_lists)
    return render.maxpain(mp,call_chains,put_chains,cv_lists,opurls_tuple,symb,current_expdate,short_name,maxcv)
    

class Free:
    def GET(self):
        """ Show page """
        user_data=web.input()
        render = create_render(session.privilege)
        
        if 'symb' in user_data.keys():
            symb=user_data.symb
            if 'expdate' in user_data.keys():
                expdate=user_data.expdate
            else:
                expdate='0'
                
            if symb in free_symb_list:
                try:
                    ompinfo=mp_index_page(symb,expdate)
                    mp=ompinfo[0]
                    call_chains=ompinfo[1]
                    put_chains=ompinfo[2]
                    cv_lists=ompinfo[3]
                    opurls_tuple=ompinfo[4]
                    current_expdate=ompinfo[5]
                    short_name=ompinfo[6]
                    maxcv=get_max_crash_value(cv_lists)
                    return render.maxpain(mp,call_chains,put_chains,cv_lists,opurls_tuple,symb,current_expdate,short_name,maxcv)
                    #get_omp_page(symb,expdate)
                    
                except Exception,e:
                    return '%s'%str(e)    
            else:
                return render.free(free_list) 
        else:
            return render.free(free_list)
        
class OptionsMaxPain:
    
    def GET(self):
        """ Show page """
        user_data=web.input()
        render = create_render(session.privilege)
        
        if 'symb' in user_data.keys():
            symb=user_data.symb
            if 'expdate' in user_data.keys():
                expdate=user_data.expdate
            else:
                expdate='0'
                
            if logged() or (symb in free_symb_list):
                try:
                    ompinfo=mp_index_page(symb,expdate)
                    mp=ompinfo[0]
                    call_chains=ompinfo[1]
                    put_chains=ompinfo[2]
                    cv_lists=ompinfo[3]
                    opurls_tuple=ompinfo[4]
                    current_expdate=ompinfo[5]
                    short_name=ompinfo[6]
                    maxcv=get_max_crash_value(cv_lists)
                    return render.maxpain(mp,call_chains,put_chains,cv_lists,opurls_tuple,symb,current_expdate,short_name,maxcv)
                    #get_omp_page(symb,expdate)
                    
                except Exception,e:
                    return '%s'%str(e)     
            else:
                raise web.seeother('/free')
               
        else:
            raise web.seeother('/')
      
class Route:
    def POST(self):
        """ Show page """
        #render = create_render(session.privilege)
        user_data = web.input()
        
        if 'symb' in user_data.keys():
            symb=user_data.symb
            
            if logged():
                try:
                    web.seeother('/omp?symb=%s'%symb)
                except Exception,e:
                    return '%s'%str(e)
            elif symb in free_symb_list:
                raise web.seeother('/omp?symb=%s'%symb) 
            else:    
                raise web.seeother('/free')
        else:
            raise web.seeother('/')
    

class Price:
    def GET(self):
        render = create_render(session.privilege)
        return render.price()

class WhatisMaxPain:
    def GET(self):
        render = create_render(session.privilege)
        return render.whatismaxpain()
                

app = web.application(urls, globals())


if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                              #initializer={'login': 0, 'privilege': 0,'user':'Guest',})
                              initializer={'login': 0, 'privilege': 0,})
                              
    web.config._session = session
else:
    session = web.config._session
### Templates

t_globals = {
    'datestr': web.datestr,
    'str':str,
    'session':session,
}
###

templates_root = os.path.join(app_root, 'templates/')
#render = web.template.render(templates_root)
render = web.template.render('templates', base='base', globals=t_globals)
render2 = web.template.render('templates', globals=t_globals)
        
application = app.wsgifunc() 

