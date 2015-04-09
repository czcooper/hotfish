# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys

free_list=[{'name':'Facebook.Inc','symb':'FB'},
           {'name':'Apple.Inc','symb':'AAPL'},
           {'name':'Microsoft Corporation','symb':'MSFT'},
           {'name':'Bank of America Corporation ','symb':'BAC'},
           {'name':'Pfizer Inc','symb':'PFE'},
           {'name':'General Electric Company','symb':'GE'},
           {'name':'Intel Corporation ','symb':'INTC'},
           {'name':'Alcoa Inc','symb':'AA'},
           {'name':'Cisco Systems, Inc','symb':'CSCO'},
           {'name':'Exxon Mobil Corporation','symb':'XOM'},
           {'name':'The Coca-Cola Company','symb':'KO'},
           {'name':'Twitter, Inc','symb':'TWTR'},
           {'name':'Zynga, Inc','symb':'ZNGA'},
           {'name':'Wells Fargo & Company','symb':'WFC'},
           {'name':'JPMorgan Chase & Co','symb':'JPM'},
           {'name':'Citigroup Inc','symb':'C'},
           {'name':'General Motors Company','symb':'GM'},
           {'name':'Tesla Motors, Inc','symb':'TSLA'},
           {'name':'Wal-Mart Stores Inc','symb':'WMT'},
           {'name':'Nike, Inc','symb':'NKE'},
           {'name':'Starbucks Corporation','symb':'SBUX'},
           {'name':'Google Inc','symb':'GOOG'},
           {'name':'FedEx Corporation','symb':'FDX'},
           {'name':'BP p.l.c','symb':'BP'},
           {'name':'Pepsico, Inc','symb':'PEP'},
           {'name':'The Goldman Sachs Group, Inc','symb':'GS'},
           {'name':'The Estée Lauder Companies Inc','symb':'EL'},
           {'name':'The Dow Chemical Company','symb':'DOW'},
           {'name':'EMC Corporation','symb':'EMC'},
           {'name':'Yahoo! Inc','symb':'YHOO'}
           ]

def get_free_symb():
    symb_list=[]
    for d in free_list:
        symb_list.append(d['symb'])
        
    #返回股票和代码字典
    #print symbdict   
    return symb_list

free_symb_list=get_free_symb()

if __name__ == "__main__":
    print free_symb_list