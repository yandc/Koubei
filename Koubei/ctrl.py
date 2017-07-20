#!/usr/bin/env python
# coding=utf-8
from redis_util import *
import datetime
import time
import zlib

def getSortedKoubei(skuIds, start, end, debug, source, dvcId):
    res = {'code':0, 'msg':'Succ', 'data':None}
    try:
        relateSet = list(set([int(x) for x in skuIds.split(',')]))
    except:
        return res
    
    result = []
    rds = RedisUtil(env='online')
    abTest = rds.get_obj('kbrank:abtest')
    strategy = 0
    if abTest and type(abTest) == list:
        hint = zlib.crc32(dvcId)&0xffffffff
        left = hint % sum(abTest)
        for i, v in enumerate(abTest):
            if left < v:
                break
            left -= v
        strategy = i
    for itemId in relateSet:
        if strategy == 0:
            key = 'koubei:rank_score:%s'%itemId
        else:
            key = 'koubei:rank_score:%s:%s'%(strategy, itemId)
        li = rds.get_obj(key)
        if not li:
            continue
        result += li
    if source == 'outline':#filter
        #auto_evaluate, positive, piclen, textlen, 
        result = [x for x in result if (x[1]!=15 and len(x)>2 and x[2] >=5 and (x[3]>0 or x[4]>20))]
    ranked = sorted(result, key=lambda x:x[1], reverse=True)
    if start >= len(ranked):
        res['data'] = []
    else:
        idList = [x[0] for x in ranked[start:end]]
        res['data'] = idList
        ts = int(time.time())
        #save expose
        if not debug:
            skuId = relateSet[0]
            dateStr = datetime.date.today().strftime('%Y%m%d')
            key = 'koubei:expose:%s:%s:%s'%(dateStr, source, skuId)
            rds.inst.rpush(key, json.dumps(idList+[dvcId, ts]))
            rds.inst.expire(key, 30*86400)#expire after 30 days
    return res

if __name__ == '__main__':
    print getSortedKoubei('1199442', 0, 10, True, 'test', '8dd7d90e7c1ca58b7f58f0bdcdf1a931')
    print getSortedKoubei('1199442', 0, 10, True, 'test', 'abc')
