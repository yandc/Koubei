#!/usr/bin/env python
# coding=utf-8
from redis_util import *
import datetime
import pdb

def getSortedKoubei(skuIds, start, end):
    res = {'code':0, 'msg':'Succ', 'data':None}
    try:
        relateSet = [int(x) for x in skuIds.split(',')]
    except:
        return res
    
    result = []
    rds = RedisUtil()
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
        #save expose
        skuId = relateSet[0]
        dateStr = datetime.date.today().strftime('%Y%m%d')
        key = 'koubei:expose:%s:%s'%(dateStr, skuId)
        rds.inst.rpush(key, json.dumps(idList))
        rds.inst.expire(key, 30*86400)#expire after 30 days
    return res

if __name__ == '__main__':
    getSortedKoubei('1307017', 0, 10)
