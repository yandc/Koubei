#!/usr/bin/env python
# coding=utf-8
from django.http import HttpResponse
from ctrl import *
import json
import urllib

def getKoubei(request):
    page = 0
    pagesize = 10
    debug = False
    dvcId = ''
    source = ''
    res = {'code':-1, 'msg':'Param error!', 'data':None}
    try:
        skuIds = urllib.unquote(request.GET['skuIds'])
        if 'page' in request.GET:
            page = int(request.GET['page'])
        if 'pagesize' in request.GET:
            pagesize = int(request.GET['pagesize'])
        if 'debug' in request.GET:
            debug = True
        if 'dvc_id' in request.GET:
            dvcId = request.GET['dvc_id']
        if 'source' in request.GET:
            source = request.GET['source']
        if page >= 0 and pagesize > 0:
            start = page * pagesize
            end = start + pagesize
            res = getSortedKoubei(skuIds, start, end, debug, source, dvcId)
    except:
        pass
    resp = HttpResponse(json.dumps(res))
    return resp

def getMaterial(request):
    page = 0
    pagesize = 10
    mtype = ''
    mids = ''
    uid = 0
    res = {'code':-1, 'msg':'Param error!', 'data':None}
    try:
        if 'page' in request.GET:
            page = int(request.GET['page'])
        if 'pagesize' in request.GET:
            pagesize = int(request.GET['pagesize'])
        if 'type' in request.GET:
            mtype = request.GET['type']
            if mtype not in ('sku', 'user', 'brand', 'category'):
                mtype = ''
        if 'ids' in request.GET:
            mids = urllib.unquote(request.GET['ids'])
        if 'uid' in request.GET:
            uid = int(request.GET['uid'])
        if page >= 0 and pagesize > 0 and mtype and mids:
            start = page * pagesize
            end = start + pagesize
            res = getSortedMaterial(mtype, mids, start, end, uid)
    except:
        pass
    resp = HttpResponse(json.dumps(res))
    return resp
