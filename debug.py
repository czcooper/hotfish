# -*- coding:utf-8 -*-
import thread,time
import logging

#定义日志
logger = logging.getLogger('zhuaqulogger') 
logger.setLevel(logging.DEBUG) 
# 创建一个handler，用于写入日志文件 
fh = logging.FileHandler('errot.log') 
#fh = logging.FileHandler('./zhuaqu.log') 
fh.setLevel(logging.DEBUG) 
# 定义handler的输出格式 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
fh.setFormatter(formatter) 
#ch.setFormatter(formatter) 
# 给logger添加handler 
logger.addHandler(fh) 

#打印日志方法
def logprint(msg):
    print msg
    logger.info(msg)
    
    
    
if __name__ == "__main__":
    pass