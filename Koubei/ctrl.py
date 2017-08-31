#!/usr/bin/env python
# coding=utf-8
from redis_util import *
import datetime
import time
import zlib

rds = RedisUtil(env='online')
abTest = [0, 10]

def getSortedKoubei(skuIds, start, end, debug, source, dvcId):
    res = {'code':0, 'msg':'Succ', 'data':None}
    try:
        relateSet = list(set([int(x) for x in skuIds.split(',')]))
    except:
        return res
    
    result = []
    #abTest = rds.get_obj('kbrank:abtest')
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
            key = 'koubei:score:%s'%itemId
        else:
            key = 'koubei:score:%s:%s'%(strategy, itemId)
        kbList = []
        idx = 0
        while True:
            jsonli = rds.inst.lindex(key, idx)
            if not jsonli:
                break
            li = json.loads(jsonli)
            if not li:
                break
            kbList += li
            if len(kbList) >= end:
                break
            else:
                idx += 1
        result += kbList
        
    if source == 'outline':#filter
        #auto_evaluate, positive, piclen, textlen, 
        result = [x for x in result if (x[1]>15 and len(x)>2 and x[2] >=5 and (x[3]>0 or x[4]>20))]
    ranked = sorted(result, key=lambda x:x[1], reverse=True)
    
    if start >= len(ranked):
        res['data'] = []
    else:
        idList = [x[0] for x in ranked[start:end]]
        res['data'] = idList
        ts = int(time.time())
        #save expose
        if not debug and source in ('outline', 'more'):
            skuId = relateSet[0]
            dateStr = datetime.date.today().strftime('%Y%m%d')
            key = 'koubei:expose:%s:%s:%s'%(dateStr, source, skuId)
            rds.inst.rpush(key, json.dumps(idList+[dvcId, ts]))
            rds.inst.expire(key, 30*86400)#expire after 30 days
    return res

def getSortedMaterial(mtype, mids, start, end):
    res = {'code':0, 'msg':'Succ', 'data':None}
    try:
        idSet = list(set([int(x) for x in mids.split(',')]))
    except:
        return res
    result = []
    for mid in idSet:
        key = 'material:%s:%s'%(mtype, mid)
        scList = []
        idx = 0
        while True:
            jsonli = rds.inst.lindex(key, idx)
            if not jsonli:
                break
            li = json.loads(jsonli)
            if not li:
                break
            scList += li
            if len(scList) >= end:
                break
            else:
                idx += 1
        result += scList
        
    ranked = sorted(result, key=lambda x:x[1], reverse=True)    
    if start >= len(ranked):
        res['data'] = []
    else:
        idList = [x[0] for x in ranked[start:end]]
        res['data'] = idList
    return res

if __name__ == '__main__':
    print getSortedMaterial('user', '1964082', 0, 10)
#    print getSortedKoubei('1238723', 0, 100, True, 'noutline', '8dd7d90e7c1ca58b7f58f0bdcdf1a931')
