#coding=utf-8
import sys
import urllib2
import re
import os
#import MySQLdb
import thread
import json
import time
#from stockskey import keystring,ccshotkey,symbdict,re_keys
#import ystockquote

type = sys.getfilesystemencoding() 
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A537a Safari/419.3')]
 
def get_org_htmlstr(baseURL):
    #baseURL='http://finance.yahoo.com/q/op?s=%s'%(symb)
    htmlstr= urllib2.urlopen(baseURL,timeout=60).read()
    
    return htmlstr

#获取默认页的期权页面数据
def get_org_data(htmlstr):
    re_key="\"data\":{\"optionData\":(.*);</script>"
    content = re.findall(re_key,htmlstr)

    opData=content[0].split('\"columns\":{\"list_table_columns\":')
    js=json.loads(opData[0].strip(','))
    
    #print js
    return js


def get_short_name(htmlstr):
    re_shortName="\"shortName\":\"(.*)\",\"longName\""
    shortName=re.findall(re_shortName,htmlstr)[0]
    
    return shortName
    

#获取特定日期的期权页面数据
def get_org_data_by_opurl(htmlstr):
    #htmlstr= urllib2.urlopen(opurl,timeout=60).read()
    re_key="\"data\":{\"optionData\":(.*);</script>"
    content = re.findall(re_key,htmlstr)
    
    opData=content[0].split('\"columns\":{\"list_table_columns\":')
    js=json.loads(opData[0].strip(','))
    
    #print js
    return js
    
#返回按Key升序后的元祖  
def sortedDictValues(adict):
    return sorted(adict.items(), key=lambda e:e[0], reverse=False)

def get_expdate_list(opurls):
    expdate_list=[]
    for opurl in opurls:
        expdate_list.append(opurl[0])
        
    #print expdate_list
    return expdate_list
        
    
def get_all_opurls(symb):
    #http://finance.yahoo.com/q/op?s=AAPL&date=1419033600
    baseURL='http://finance.yahoo.com/q/op?s=%s'%(symb)
    htmlstr=get_org_htmlstr(baseURL)
    js=get_org_data_by_opurl(htmlstr)
    
    expDates=js['expirationDates']
    epochs=js['epochs']
    #print expDates
    #print epochs
    
    """
    opurls=[]
    for i in range(len(expDates)):
        exd=expDates[i][:10]
        url='http://finance.yahoo.com/q/op?s=%s&date=%s'%(symb,epochs[i])
        opurl={
               'expDate':exd,
               'url':url,
               }
        
        opurls.append(opurl)
    """
    opurls={}
    for i in range(len(expDates)):
        exd=expDates[i][:10]
        url='http://finance.yahoo.com/q/op?s=%s&date=%s'%(symb,epochs[i])
        opurls[exd]=url
    
    #转成元祖
    #new_opurls=sorted(opurls.iteritems(), key=lambda d:d[0],reverse=False)
    #return new_opurls
    #返回按Key排序后的元祖
    #print sortedDictValues(opurls)
    #return sortedDictValues(opurls)
    #返回为字典
    return opurls
        

#从原始网页获取call链和put链        
def get_chains_by_type(chains,type):
    type_chains=[]
    
    for chain in chains:
        dict_chain={
                   'strike':float(chain['strike']),
                   'contract':chain['contractSymbol'],
                   'last':chain['lastPrice'],
                   'bid':chain['bid'],
                   'ask':chain['ask'],
                   'change':chain['change'],
                   'percentchange':chain['percentChangeRaw'],
                   'volume':int(chain['volume']),
                   'openinterest':int(chain['openInterest']),
                   'impliedvolatility':chain['impliedVolatility'],
                   'inTheMoney':chain['inTheMoney'], 
                   'type':type,                  
                   } 
        type_chains.append(dict_chain) 
           
    #print type_chains
    #print len(type_chains)
    return type_chains

#拆分出call 链和put 链
def use_chains_by_type(chains,type):
    type_chains=[]
    for chain in chains:
        if chain['type']==type:
            type_chains.append(chain)
    
    return type_chains   

#具体期权日的所有期权链，Call和Put
def get_all_chain_list(htmlstr):
    js=get_org_data_by_opurl(htmlstr)
    #chains = get_all_opurls(symb,js)
    options=js['options']
    
    puts=options['puts']
    calls=options['calls']
    #print len(puts)
    #print len(calls)
    
    allchains=get_chains_by_type(calls,'call')
    puts_chains=get_chains_by_type(puts,'put')
    
    allchains.extend(puts_chains)
    
    #print allchains
    #print len(allchains)
    return allchains
    
def get_uprice(allchain):
    #获得uprice价格列表
    uprice=[]
    for strike in allchain:
        #print strike
        uprice.append(strike['strike'])
    uprice={}.fromkeys(uprice).keys() #列表去重
    
    uprice.sort()
    
    uprice
    return uprice

#单个价值，用户不可见
def get_crash_value(uprice,allchain):
    
    callvalue=0
    putvalue=0
    totalvalue=0
    for chain in allchain:
        #print chain
        if chain['type']=='call' and chain['strike']<uprice:
            callvalue+=(uprice-chain['strike'])*chain['openinterest']
            #print chain['OI']
            #print callvalue
        elif chain['type']=='put' and chain['strike']>uprice:
            putvalue+=(chain['strike']-uprice)*chain['openinterest']
    cv={
        'uprice':uprice,
        'callvalue':callvalue,
        'putvalue':putvalue,
        'totalvalue':callvalue+putvalue
        }
    
    #print cv
    return cv

#所有价值，用户不可见
def get_all_crash_value(allchains):

    #allchains=get_all_chain_list(opurl)
    
    crash_value_list=[]
    uprice=get_uprice(allchains)
    
    for price in uprice:
        cv=get_crash_value(price,allchains)
        crash_value_list.append(cv)
    
    #print crash_value_list
    return crash_value_list

def get_mp_price(allchains):
    cvlist=get_all_crash_value(allchains)
    
    #初始化一个值，好比较
    mpvalue=cvlist[0]['totalvalue']
    mp=cvlist[0]['uprice']
    for cv in cvlist:
        if cv['totalvalue']<mpvalue:
            mpvalue=cv['totalvalue']
            mp=cv['uprice']
    
    #print mp
    return mp
    

def mp_index_page(symb,expdate):
    
    #baseURL='http://finance.yahoo.com/q/op?s=%s'%(symb)
    all_opurls=get_all_opurls(symb)
    #把all_opurl转换为元祖后返回
    opurls_tuple=sortedDictValues(all_opurls)
    
    if all_opurls.has_key(expdate):
        current_expdate=expdate
        t_opurl=all_opurls[expdate]
    else:
        #如果没有expdate则取第一个日期为默认值
        #url_list=all_opurls.items()
        current_expdate=opurls_tuple[0][0]
        t_opurl=opurls_tuple[0][1]
    
    #t_opurl 只用在all_chains 方法中，其它计算都基于all_chains
    htmlstr=get_org_htmlstr(t_opurl)
    short_name=get_short_name(htmlstr)
    all_chains=get_all_chain_list(htmlstr)
    
    #获取所有crash value列表
    cv_lists=get_all_crash_value(all_chains)
    #获取mp值
    mp=get_mp_price(all_chains)
    
    #获取call options链
    call_chains=use_chains_by_type(all_chains,'call')
    #获取put options链
    put_chains=use_chains_by_type(all_chains,'put')
    
    
    return [mp,call_chains,put_chains,cv_lists,opurls_tuple,current_expdate,short_name]


if __name__ == "__main__":
    print mp_index_page('FB','0')
    #mp_date_page('MS','2015-03-20')
    #print test()
    #print get_all_opurls('QIHU')