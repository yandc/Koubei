#!/usr/bin/python
# -*- coding: utf-8 -*-
import redis
from rediscluster import client
import datetime
import json


class RedisUtil:
    def __init__(self, env='test'):
        nodes = {
            'test':[
                {'host': '10.1.106.26', 'port': 7000},
                {'host': '10.1.106.26', 'port': 7001},
                {'host': '10.1.106.26', 'port': 7002},
                {'host': '10.1.106.38', 'port': 7000},
                {'host': '10.1.106.38', 'port': 7001},
                {'host': '10.1.106.38', 'port': 7002},
            ],
            'online':[
                {'host': '10.1.117.110', 'port':7300},
                {'host': '10.1.13.11', 'port':7302},
                {'host': '10.1.13.11', 'port':7300},
                {'host': '10.1.117.110', 'port':7301},
                {'host': '10.1.13.11', 'port':7301},
                {'host': '10.1.117.110', 'port':7302}
            ]
        }
        pool = client.ClusterConnectionPool(startup_nodes=nodes[env])
        self.inst = client.StrictRedisCluster(connection_pool=pool)
        #self.inst = redis.StrictRedis(host=host, port=port, db=0)

    def get_number(self, key):
        key = str(key)
        if self.inst.exists(key):
            return int(self.inst.get(key))
        else:
            self.inst.set(key, 0)
            return 0
        
    def set_number(self, key, value):
        key = str(key)
        self.inst.set(key, str(value))
        
    def get_obj(self, key):
        key = str(key)
        if self.inst.exists(key):
            return json.loads(self.inst.get(key))
        else:
            return None
        
    def set_obj(self, key, value):
        key = str(key)
        self.inst.set(key, json.dumps(value))

    def get(self, key):
        return self.inst.get(key)
    
    def set(self, key, value):
        return self.inst.set(key, value)

    def keys(self, keys):
        return self.inst.keys(keys)

    def delete(self, key):
        return self.inst.delete(key)


if __name__ == '__main__':
    redis = RedisUtil()
    tt = redis.get('ethspy:lastOnlineTime')
    print tt
