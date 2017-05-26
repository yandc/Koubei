#!/usr/bin/env python
# coding=utf-8
from django.http import HttpResponse
from ctrl import *
import json
import urllib

def getKoubei(request):
    page = 0
    pagesize = 10
    res = {'code':-1, 'msg':'Param error!', 'data':None}
    try:
        skuIds = urllib.unquote(request.GET['skuIds'])
        if 'page' in request.GET:
            page = int(request.GET['page'])
        if 'pagesize' in request.GET:
            pagesize = int(request.GET['pagesize'])
        if 'debug' in request.GET:
            debug = True
        else:
            debug = False
        if page >= 0 and pagesize > 0:
            start = page * pagesize
            end = start + pagesize
            res = getSortedKoubei(skuIds, start, end, debug)
    except:
        pass
    resp = HttpResponse(json.dumps(res))
    return resp
