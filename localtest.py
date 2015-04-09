from omp_maxpain import get_all_opurls
from free_db import free_list,free_symb_list

def test():
    get_all_opurls('MS')
    #get_all_chain_list()

def sortedDictValues(adict):
    keys = adict.keys()
    keys.sort(reverse=False)
    #return [adict[key] for key in keys]
    return [(key,adict[key]) for key in keys]

def sortedDictValues2(adict): 
    keys = adict.keys() 
    keys.sort() 
    return map(adict.get,keys)

def sortedDictValues3(adict): 
    return sorted(adict.items(), key=lambda e:e[0], reverse=False)

def test2():
    d={'2015-03-23':'url','2015-02-21':'y','2015-10-05':'10010'}
    dl=('shfjdfds0','sfjiffd1','sfufsdfd2','shfjdfds3','sfjiffd4','sfufsdfd5','shfjdfds6','sfjiffd7','sfufsdfd8','shfjdfds9','sfjiffd10','sfufsdfd11')
    #print len(d)
    #print sortedDictValues2(d)
    #print sortedDictValues3(d)
    d4=3
    #print dl[:2]
    #print dl[:(d4*1)]
    dd4=sortedDictValues3(d)
    print dd4
    print dd4[0][1]
    url_list=d.items()
    print url_list


    
    #print url

if __name__ == "__main__":
    test2()