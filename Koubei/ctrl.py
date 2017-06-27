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
    print getSortedKoubei('1185761', 0, 10, True, 'test', 'abc')
