#!/usr/bin/env python
# coding=utf-8
from django.http import HttpResponse
from ctrl import *
import json

def getKoubei(request):
    page = 0
    pagesize = 10
    res = {'code':-1, 'msg':'Param error!', 'data':None}
    try:
        skuIds = request.GET['skuIds']
        if 'page' in request.GET:
            page = int(request.GET['page'])
        if 'pagesize' in request.GET:
            pagesize = int(request.GET['pagesize'])
        if page >= 0 and pagesize > 0:
            start = page * pagesize
            end = start + pagesize
            res = getSortedKoubei(skuIds, start, end)
    except:
        pass
    resp = HttpResponse(json.dumps(res))
    return resp
