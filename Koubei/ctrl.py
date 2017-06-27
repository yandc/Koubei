#!/usr/bin/env python
# coding=utf-8
from redis_util import *
import datetime
import time

def getSortedKoubei(skuIds, start, end, debug, source, dvcId):
    res = {'code':0, 'msg':'Succ', 'data':None}
    try:
        relateSet = list(set([int(x) for x in skuIds.split(',')]))
    except:
        return res
    
    result = []
    rds = RedisUtil(env='online')
    for itemId in relateSet:
        key = 'koubei:rank_score:%s'%itemId
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
    print getSortedKoubei('1185761', 0, 10, True)
